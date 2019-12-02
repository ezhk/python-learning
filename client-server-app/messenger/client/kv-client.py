#!/usr/bin/env python

from binascii import hexlify, unhexlify
from functools import partial
from logging import getLogger
from io import BytesIO, StringIO
import sys

sys.path.append(".")

from PIL import Image as PILImage, ImageDraw
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.image import Image, CoreImage
from kivy.core.image.img_pil import ImageLoaderPIL
from kivy.clock import Clock

from kivy.properties import (
    BooleanProperty,
    StringProperty,
    ListProperty,
    ObjectProperty,
)
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.widget import Widget

import jim.logger
from jim.classes import Client
from jim.utils import parse_arguments


class SelectableRecycleBoxLayout(
    FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout
):
    """ Adds selection and focus behaviour to the view. """


class SelectableLabel(RecycleDataViewBehavior, Label):
    """
    Add selection support to the Label.
    """

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app = App.get_running_app()
        self.root_widget = app.root

    def refresh_view_attrs(self, rv, index, data):
        """
        Catch and handle the view changes.
        """

        self.index = index
        return super().refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ 
        Add selection on touch down.
        """

        if super().on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """
        Respond to the selection of items in the view.
        """

        self.selected = is_selected
        if is_selected:
            try:
                self.root_widget.set_active_chat(rv.data[index].get("text"))
            except:
                pass


class Contacts(RecycleView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = []


class Chat(RecycleView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = []


class AuthPopup(Popup):
    username = StringProperty()
    password = StringProperty()

    def __init__(self, widget, **kwargs):
        super().__init__(**kwargs)
        self.widget = widget

    def save(self):
        self.widget.auth(self.username, self.password)
        self.dismiss()


class LoadImage(Popup):
    """
    Parent is UserpicEditor,
    when push Open button in UserpicEditor
    open this popup with crop function.

    Class has only one specified method - load,
    it calls for parent load_preview with iamge path.
    """

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window

    def load(self, selection):
        filepath = selection.pop()
        self.window.load_preview(filepath)
        self.dismiss()

    def cancel(self):
        self.dismiss()


class UserpicEditor(Popup):
    image = ObjectProperty(None)

    x1 = StringProperty()
    y1 = StringProperty()
    x2 = StringProperty()
    y2 = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        app = App.get_running_app()
        self.root_widget = app.root

        self.load_image_popup = LoadImage(self)

        # define original and crop images
        self.pil_image = None
        self.cropped_image = None

    def _draw_image(self, image=None):
        image = image if image else self.pil_image
        if not image:
            return

        texture = None
        with BytesIO() as output:
            image.save(output, format="PNG")
            output.seek(0)
            texture = CoreImage(output, ext="png").texture
        if not texture:
            return

        self.image.source = ""
        self.image.texture = texture
        self.image.reload()

    def load_preview(self, filepath):
        """
        Load image from file path and draw it.
        """

        self.pil_image = PILImage.open(filepath)
        self._draw_image()

    def crop(self):
        """
        Crop image with rectangle coors: (x1, y1) and (x2, y2).
        """

        self.cropped_image = self.pil_image.crop(
            (int(self.x1), int(self.y1), int(self.x2), int(self.y2))
        )
        self._draw_image(self.cropped_image)

    def save(self):
        """
        Store image into database.
        """

        self.root_widget.update_userpic(self.cropped_image or self.pil_image)
        self.dismiss()

    def push_load_image(self):
        self.load_image_popup.open()


class AddContact(Popup):
    contact = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        app = App.get_running_app()
        self.root_widget = app.root

    def save(self, *args):
        if self.contact:
            self.root_widget.add_contact(self.contact)
        self.contact = ""
        self.dismiss()


class DelContact(Popup):
    contact = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        app = App.get_running_app()
        self.root_widget = app.root

    def save(self, *args):
        if self.contact:
            self.root_widget.del_contact(self.contact)
        self.contact = ""
        self.dismiss()


class ErrorPopup(Popup):
    message = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = ""

    def set_message(self, message):
        self.message = message

    def close(self):
        app = App.get_running_app()
        app.stop()


class NotificationPopup(Popup):
    message = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = ""

    def set_message(self, message):
        self.message = message


class RootWidget(Widget):
    userpic = ObjectProperty(None)
    username = StringProperty()

    chat_with = StringProperty()

    chat_messages = StringProperty()
    contact_list = ListProperty()

    input_text = StringProperty()

    def __init__(self, opts, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # external arsed options
        self.opts = opts

        # client object defined in auth section
        self.client = None

        # authentifiaction popup with login and passowrd
        self.auth_popup = AuthPopup(self)

        # Popup with messages data
        self.notification_popup = NotificationPopup()
        self.error_popup = ErrorPopup()

        # default chat labels
        self.username = "Anonymous"
        self.chat_with = "Chat"

    def auth(self, username, password):
        self.client = Client(
            self.opts.address,
            self.opts.port,
            username,
            password,
            kivy_object=self,
            logger=getLogger("messenger.client"),
        )
        self.client.start()

    def emit_chat(self, messages, *args):
        self.chat_messages = ""

        tmp_messages = []
        for message in messages:
            tmp_messages.append(
                f"{message['from']} > {message['to']}"
                + f"@ {message['ctime']}:",
            )
            tmp_messages.append(f"{message['text']}")
        self.chat_messages = "\n".join(tmp_messages)

    def emit_contacts(self, contacts, *args):
        self.contact_list = []
        for contact in contacts:
            self.contact_list.append({"text": contact})

    def emit_profile(self, profile, *args):
        """
        Function update profile info in Root windget:
        - userpic
        - username
        when "update_profile" action has received.

        Also request contacts after processing profile.
        """

        def _draw_userpic(image):
            """
            Accept PIL image presentation and convert it by size,
            draw in userpic area.
            """
            image = image.resize((70, 70), PILImage.BILINEAR)
            if not image:
                return

            texture = None
            with BytesIO() as output:
                image.save(output, format="PNG")
                output.seek(0)
                texture = CoreImage(output, ext="png").texture
            if not texture:
                return

            self.userpic.source = ""
            self.userpic.texture = texture
            self.userpic.reload()
            if profile is None:
                return

        # update username
        self.username = profile.get("username", "anonimous").capitalize()

        # update userpic
        image = None
        if profile.get("userpic", None) is None:
            image = PILImage.open("ui/images/userpic.png")
        else:
            raw_image = unhexlify(profile.get("userpic").encode())
            stream = BytesIO(raw_image)
            image = PILImage.open(stream)
        _draw_userpic(image)

        # request contacts for user
        self.client._get_contacts()

    def emit_notification(self, message, *args):
        self.notification_popup.set_message(message[:96])
        self.notification_popup.open()

    def emit_error(self, message, *args):
        self.error_popup.set_message(message[:96])
        self.error_popup.open()

    def emit(self, message):
        """
        Caught external emit signal and run Clock.
        Why do we use Clock? When call update_profile from client thread
        CoreImage class in _draw_userpic caise "segmantation fault".
        """

        if message.get("action", None) == "update_chat":
            return Clock.schedule_once(
                partial(self.emit_chat, message.get("data", [])), 0
            )

        if message.get("action", None) == "update_contacts":
            return Clock.schedule_once(
                partial(self.emit_contacts, message.get("data", [])), 0
            )

        if message.get("action", None) == "update_profile":
            return Clock.schedule_once(
                partial(self.emit_profile, message.get("data", {})), 0
            )

        if message.get("action", None) == "background_message":
            message = f"Received message from {message['from']}:\n{message['message']}"
            return Clock.schedule_once(
                (partial(self.emit_notification, message)), 0
            )

        if message.get("error", None) is not None:
            return Clock.schedule_once(
                partial(self.emit_error, message.get("error")), 0
            )

    def set_active_chat(self, username):
        self.client.active_chat = username
        self.chat_with = f"Chat with {username}"

        self.client._get_chat(username)

    def update_userpic(self, image):
        if not image:
            return
        with BytesIO() as output:
            image = image.resize((30, 30), PILImage.BILINEAR)
            image.save(output, format="PNG")
            self.client._upload_userpic(hexlify(output.getvalue()).decode())

    def push_message(self):
        """
        "Send message" button event:
        - calls "send message" and store msg into database
        - get actual user chat
        """

        message = self.input_text
        try:
            self.client._send_message(self.client.active_chat, message)
            self.client._get_chat(self.client.active_chat)
        except Exception:
            pass

        # clean input form
        self.input_text = ""

    def add_contact(self, username):
        """
        Func calls remote add user in database
        and call function "get actual contact list".
        """
        self.client._add_contact(username)
        return self.client._get_contacts()

    def del_contact(self, username):
        """
        Func calls remote delete user in database
        and call function "get actual contact list".
        """

        self.client._delete_contact(username)
        return self.client._get_contacts()


class ClientApp(App):
    def __init__(self, opts, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opts = opts

    def build(self, *args, **kwargs):
        super().build(*args, **kwargs)
        return RootWidget(self.opts)

    def on_start(self, *args, **kwargs):
        super().on_start(*args, **kwargs)
        self.root.auth_popup.open()


if __name__ == "__main__":
    opts = parse_arguments()
    ClientApp(opts).run()
