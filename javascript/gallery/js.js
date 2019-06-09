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
        openedImageArrowRotate: 'galleryWrapper__arrowsRotate',
        openedImageScreenClass: 'galleryWrapper__screen',
        openedImageCloseBtnClass: 'galleryWrapper__close',
        openedImageCloseBtnSrc: 'images/gallery/close.png',
        leftArrowImage: 'images/left-arrow.svg',
        /*
         * rightArrowImage не используется, вместо него используется стрелка влево с rotate()
         * rightArrowImage: 'images/right-arrow.svg',
         */
        unknownImage: 'images/unknown-image.svg',
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
        imageSelector.src = this.settings.unknownImage;

        // Получаем контейнер для открытой картинки, в нем находим тег img и ставим ему нужный src.
        // this.getScreenContainer().querySelector(`.${this.settings.openedImageClass}`).src = src;
    },

    /**
     * Проверяет, что изображение доступно по указанному атрибуту src=""
     * @param {string} imageLocation — путь к изображение
     * @return {boolean} — если 200 статус код, то картинка доступна
     */
    imageExist(imageLocation) {
        const httpRequest = new XMLHttpRequest();
        httpRequest.open("HEAD", imageLocation, false);
        httpRequest.send();

        return httpRequest.status === 200;
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
        galleryWrapperElement.appendChild(this.createCloseElement());

        // Создаем контейнер для стрелок и изображения
        const imageContainer = this.createImageContainer();
        galleryWrapperElement.appendChild(imageContainer);

        // создаем стрелку влево, место для картинки и стрелку вправо
        imageContainer.appendChild(this.createArrow('left'));
        imageContainer.appendChild(this.createImagePlace());
        imageContainer.appendChild(this.createArrow('right'));

        // Добавляем контейнер-обертку в тег body.
        document.body.appendChild(galleryWrapperElement);

        // Возвращаем добавленный в body элемент, наш контейнер-обертку.
        return galleryWrapperElement;
    },

    /**
     * Создает элемент стрелку и возвращает его
     * @return {HTMLImageElement}
     */
    createCloseElement() {
        const closeImageElement = new Image();
        closeImageElement.classList.add(this.settings.openedImageCloseBtnClass);
        closeImageElement.src = this.settings.openedImageCloseBtnSrc;
        closeImageElement.addEventListener('click', () => this.close());
        return closeImageElement;
    },

    /**
     * Создает контейнер для изображения, ставим класс и добавляем обработчик
     * @param {MouseEvent} event — событие клика мышкой
     * @return {HTMLElement} — div контейнер для стрелок и изображения
     */
    createImageContainer() {
        const imageContainer = document.createElement('div');
        imageContainer.classList.add(this.settings.openedImageBlock);
        imageContainer.addEventListener('click',
            event => this.imageSwitcherContainer(event));

        return imageContainer;
    },

    /**
     * Создает стрелку
     * @param {string} type — тип стрелки: left (влево) или right (вправо)
     * @return {HTMLImageElement} — изображение со стрелкой
     */
    createArrow(type) {
        const arrow = new Image();
        arrow.classList.add(this.settings.openedImageArrow);
        switch (type) {
            case 'left':
                arrow.src = this.settings.leftArrowImage;
                break;
            case 'right':
                // Немного оптимизации, чтобы не грузить стрелку "вправо", мы поворачиваем стрелку "влево"
                arrow.src = this.settings.leftArrowImage;
                arrow.classList.add(this.settings.openedImageArrowRotate);
                break;
        }

        return arrow;
    },

    /**
     * Создает место для изображения и добавляет класс
     * @return {HTMLImageElement} — возвражение <img> тега
     */
    createImagePlace() {
        const image = new Image();
        image.classList.add(this.settings.openedImageClass);

        return image;
    },

    /**
     * Закрывает (удаляет) контейнер для открытой картинки.
     */
    close() {
        document.querySelector(`.${this.settings.openedImageWrapperClass}`).remove();
    },

    /**
     * Event событие по клику мышки на левую или правую часть изображения/экрана
     * @param {MouseEvent} event — событие по клику мышки
     */
    imageSwitcherContainer(event) {
        event.stopPropagation();

        const direction = this.getImageDirection(event);
        let imageSelector = this.getScreenContainer()
            .querySelector(`.${this.settings.openedImageClass}`);
        const image = this.getImageByDirection(imageSelector, direction);

        this.openImage(image);
    },

    /**
     * Опредеояет в какую часть экрана кликнул пользователь;
     * если в правую, то следующая картинка; если в левую, то предыдущая
     * @param {MouseEvent} event — берет полочение курсора при клике
     * @return {string} — какую картинку показать next или prev
     */
    getImageDirection(event) {
        return window.innerWidth / event.layerX < 2 ? 'next' : 'prev';
    },

    /**
     * Берет все изображения и в зависимости от того, где был клик мышки
     *   возвращает соответствующую картинку
     * @param {Node} imageSelector — селектор изображения
     * @param {string} direction — prev/next
     * @return {string} — ссылка на картинку
     */
    getImageByDirection(imageSelector, direction) {
        const images = this.getAllImages();
        switch (direction) {
            case 'next':
                return this.getNextImageSource(imageSelector, images);
            case 'prev':
                return this.getPrevImageSource(imageSelector, images);
        }
    },

    /**
     * Получает все изображения по атрибуту data-full_image_url
     * @return {string[]} — список со строками ссылок к изображениям
     */
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

    /**
     * Выбирает следующую картинку из списка ихображений, производя поиск индекса
     * @param {Node} imageSelector — текущее изображение
     * @param {string[]}  images — список изображений
     * @return {string} ссылку на картинку
     */
    getNextImageSource(imageSelector, images) {
        let nextIdx = images.indexOf(imageSelector.dataset.rawSource);
        if (nextIdx++ < 0) {
            return this.settings.unknownImage;
        }
        return images[nextIdx % images.length];
    },

    /**
     * Выбирает предыдущую картинку из списка ихображений, производя поиск индекса
     * @param {Node} imageSelector — текущее изображение
     * @param {string[]}  images — список изображений
     * @return {string} ссылку на картинку
     */
    getPrevImageSource(imageSelector, images) {
        let prevIdx = images.indexOf(imageSelector.dataset.rawSource);
        if (prevIdx-- < 0) {
            return this.settings.unknownImage;
        }
        while (prevIdx < 0) {
            prevIdx += images.length;
        }
        return images[prevIdx % images.length];
    },
};

// Инициализируем нашу галерею при загрузке страницы.
window.onload = () => gallery.init({previewSelector: '.galleryPreviewsContainer'});