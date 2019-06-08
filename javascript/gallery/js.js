"use strict";

/**
 * @property {Object} settings Объект с настройками галереи.
 * @property {string} settings.previewSelector Селектор обертки для миниатюр галереи.
 * @property {string} settings.openedImageWrapperClass Класс для обертки открытой картинки.
 * @property {string} settings.openedImageClass Класс открытой картинки.
 * @property {string} settings.openedImageScreenClass Класс для ширмы открытой картинки.
 * @property {string} settings.openedImageCloseBtnClass Класс для картинки кнопки закрыть.
 * @property {string} settings.openedImageCloseBtnSrc Путь до картинки кнопки открыть.
 */
const gallery = {
    settings: {
        previewSelector: '.mySuperGallery',
        openedImageWrapperClass: 'galleryWrapper',
        openedImageBlock: 'galleryWrapper__block',
        openedImageClass: 'galleryWrapper__image',
        openedImageArrow: 'galleryWrapper__arrows',
        openedImageScreenClass: 'galleryWrapper__screen',
        openedImageCloseBtnClass: 'galleryWrapper__close',
        openedImageCloseBtnSrc: 'images/gallery/close.png',
        leftArrowImage: 'images/left-arrow.svg',
        rightArrowImage: 'images/right-arrow.svg',
    },

    /**
     * Инициализирует галерею, ставит обработчик события.
     * @param {Object} userSettings Объект настроек для галереи.
     */
    init(userSettings = {}) {
        // Записываем настройки, которые передал пользователь в наши настройки.
        Object.assign(this.settings, userSettings);

        // Находим элемент, где будут превью картинок и ставим обработчик на этот элемент,
        // при клике на этот элемент вызовем функцию containerClickHandler в нашем объекте
        // gallery и передадим туда событие MouseEvent, которое случилось.
        document
            .querySelector(this.settings.previewSelector)
            .addEventListener('click', event => this.containerClickHandler(event));
    },

    /**
     * Обработчик события клика для открытия картинки.
     * @param {MouseEvent} event Событие клики мышью.
     * @param {HTMLElement} event.target Целевой объект, куда был произведен клик.
     */
    containerClickHandler(event) {
        // Если целевой тег не был картинкой, то ничего не делаем, просто завершаем функцию.
        if (event.target.tagName !== 'IMG') {
            return;
        }
        // Открываем картинку с полученным из целевого тега (data-full_image_url аттрибут).
        this.openImage(event.target.dataset.full_image_url);
    },

    /**
     * Открывает картинку.
     * @param {string} src Ссылка на картинку, которую надо открыть.
     */
    openImage(src) {
        let imageSelector = this.getScreenContainer()
            .querySelector(`.${this.settings.openedImageClass}`);
        imageSelector.dataset.rawSource = src;

        if (this.imageExist(src)) {
            return imageSelector.src = src;
        }
        imageSelector.src = this.settings.leftArrowImage;

        // Получаем контейнер для открытой картинки, в нем находим тег img и ставим ему нужный src.
        // this.getScreenContainer().querySelector(`.${this.settings.openedImageClass}`).src = src;
    },

    imageExist(imageLocation) {
        console.log(imageLocation);
        const httpRequest = new XMLHttpRequest();
        httpRequest.open("HEAD", imageLocation, false);
        httpRequest.send();

        return httpRequest.status === 200 ? true : false;
    },

    /**
     * Возвращает контейнер для открытой картинки, либо создает такой контейнер, если его еще нет.
     * @returns {Element}
     */
    getScreenContainer() {
        // Получаем контейнер для открытой картинки.
        const galleryWrapperElement = document.querySelector(`.${this.settings.openedImageWrapperClass}`);
        // Если контейнер для открытой картинки существует - возвращаем его.
        if (galleryWrapperElement) {
            return galleryWrapperElement;
        }

        // Возвращаем полученный из метода createScreenContainer контейнер.
        return this.createScreenContainer();
    },

    /**
     * Создает контейнер для открытой картинки.
     * @returns {HTMLElement}
     */
    createScreenContainer() {
        // Создаем сам контейнер-обертку и ставим ему класс.
        const galleryWrapperElement = document.createElement('div');
        galleryWrapperElement.classList.add(this.settings.openedImageWrapperClass);

        // Создаем контейнер занавеса, ставим ему класс и добавляем в контейнер-обертку.
        const galleryScreenElement = document.createElement('div');
        galleryScreenElement.classList.add(this.settings.openedImageScreenClass);
        galleryWrapperElement.appendChild(galleryScreenElement);

        // Создаем картинку для кнопки закрыть, ставим класс, src и добавляем ее в контейнер-обертку.
        const closeImageElement = new Image();
        closeImageElement.classList.add(this.settings.openedImageCloseBtnClass);
        closeImageElement.src = this.settings.openedImageCloseBtnSrc;
        closeImageElement.addEventListener('click', () => this.close());
        galleryWrapperElement.appendChild(closeImageElement);

        // Создаем контейнер для стрелок и изображения, ставим класс и добавляем обработчик
        const imageArrows = document.createElement('div');
        imageArrows.classList.add(this.settings.openedImageBlock);
        imageArrows.addEventListener('click', event => this.imageSwitcherContainer(event));
        galleryWrapperElement.appendChild(imageArrows);

        // создаем стрелку влево
        const leftArrow = new Image();
        leftArrow.classList.add(this.settings.openedImageArrow);
        leftArrow.src = this.settings.leftArrowImage;
        imageArrows.appendChild(leftArrow);

        // Создаем картинку, которую хотим открыть и добавляем ее в контейнер-обертку.
        const image = new Image();
        image.classList.add(this.settings.openedImageClass);
        imageArrows.appendChild(image);

        // создаем стрелку вправо
        const rightArrow = new Image();
        rightArrow.classList.add(this.settings.openedImageArrow);
        rightArrow.src = this.settings.rightArrowImage;
        imageArrows.appendChild(rightArrow);

        // Добавляем контейнер-обертку в тег body.
        document.body.appendChild(galleryWrapperElement);

        // Возвращаем добавленный в body элемент, наш контейнер-обертку.
        return galleryWrapperElement;
    },

    /**
     * Закрывает (удаляет) контейнер для открытой картинки.
     */
    close() {
        document.querySelector(`.${this.settings.openedImageWrapperClass}`).remove();
    },

    imageSwitcherContainer(event) {
        event.stopPropagation();

        const direction = this.getImageDirection(event);
        let imageSelector = this.getScreenContainer()
            .querySelector(`.${this.settings.openedImageClass}`);
        const image = this.getImageByDirection(imageSelector, direction);

        this.openImage(image);
    },

    getImageDirection(event) {
        return window.innerWidth / event.layerX < 2 ? 'next' : 'prev';
    },

    getImageByDirection(imageSelector, direction) {
        const images = this.getAllImages();
        switch (direction) {
            case 'next':
                return this.getNextImageSource(imageSelector, images);
            case 'prev':
                return this.getPrevImageSource(imageSelector, images);
        }
    },

    getAllImages() {
        const images = [];
        for (let element of document
            .querySelector(this.settings.previewSelector)
            .querySelectorAll('img')) {
            if (element.dataset.full_image_url) {
                images.push(element.dataset.full_image_url);
            }
        }

        return images;
    },

    getNextImageSource(imageSelector, images) {
        let nextIdx = images.indexOf(imageSelector.dataset.rawSource);
        if (nextIdx++ < 0) {
            return;
        }
        return images[nextIdx % images.length];
    },

    getPrevImageSource(imageSelector, images) {
        let prevIdx = images.indexOf(imageSelector.dataset.rawSource);
        if (prevIdx-- < 0) {
            return;
        }
        while (prevIdx < 0) {
            prevIdx += images.length;
        }
        return images[prevIdx % images.length];
    },
};

// Инициализируем нашу галерею при загрузке страницы.
window.onload = () => gallery.init({previewSelector: '.galleryPreviewsContainer'});