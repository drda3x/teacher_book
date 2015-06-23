/**
 * Класс для работы Popover'a в меню присутствия учеников на занятиях
 */

if(!window.vidgetsLogic) window.vidgetsLogic = {};

window.vidgetsLogic.Popover = (function($) {

    /**
     * Класс определяющий поведение popover'a
     * @constructor
     */
    function Popover() {
        this.html = $('#pass_menu').html();
        this.objSelector = '.popover';
        this.activeClass = 'popover-opened';
    }

    /**
     * Инициализируем popover для объекта
     * @param $target
     */
    Popover.prototype.init = function($target) {
        $target.popover({content: this.html, html: true, trigger: 'manual', animation: false});
    };

    /**
     * Получить сохраненное значение
     * @returns {*}
     */
    Popover.prototype.getExistedValue = function() {
        return this.$target.attr('val');
    };

    /**
     * Спрятать popover
     * @param timeout
     */
    Popover.prototype.hide = function(timeout) {
        if(this.$object) {
            this.$object.hide(timeout || 0);
            setTimeout(this.$object.remove, timeout || 0);
        }
    };

    /**
     * Показать popover
     * @param $target
     */
    Popover.prototype.show = function($target) {

        var self = this;

        // Если открываем popover для ячейки для которой он еще не открыт
        // иначе просто удаляем класс "popover-opened"(self.activeClass)
        // как следствие - popover просто закроется
        if(!$target.hasClass(self.activeClass)) {

            // init
            self.$target = $target;
            self.$container = $target.parent();
            self.$target.popover('show');
            self.$object = self.$container.find(self.objSelector);

            // Если нужно устанавливаем уже существующее значение
            var value = self.getExistedValue();
            if(value) {
                this.$object.find('input[value='+value+']').prop('checked', 'checked');
            }

            // Вешаем евенты
            self.$object.find('input').click(function() {
                var $this = $(this),
                    newValue = $this.val();

                // Если кликнули по выделленному input'y - нужно снять с него фокус и обнулить контейнер данных
                if(newValue == self.getExistedValue()) {
                    $this.prop('checked', false);
                    self.$target.removeAttr('val');
                } else {
                    self.$target.attr('val', newValue);
                }
            });

            // Класс с активным попапом может быть только один, так что сначала удалим все классы,
            // а потом поставим класс "popover-opened"(self.activeClass) в текущий $target
            $('body').find('.'+self.activeClass).each(function() {
                $(this).removeClass(self.activeClass);
            });

            self.$target.addClass(self.activeClass);
        } else {
            self.$target.removeClass(this.activeClass);
        }
    };

    return Popover

})(window.jQuery);