(function($) {

    // functions
    function classCheck(elem, classname) {
        if (!elem.hasClass(classname)) {
            elem.addClass(classname);
        } else {
            elem.removeClass(classname);
        }
    }

    // Tabs
    function Tabs() {
        var tabContainer = $('[data-role="tab"]');
        tabContainer.hide().filter(':first').show();

        $('[data-role="tab-trigger"]').click(function () {
            tabContainer.hide();
            tabContainer.filter(this.hash).show();
            $('[data-role="tab-trigger"]').removeClass('active');
            $(this).addClass('active');
            return false;
        }).filter(':first').click();
    }

    function classCheckByTrigger(elem, trigger, classname) {
        trigger.click(function() {
            classCheck(elem, classname);
        });
    }

    // ProductsViewType
    function ProductsViewType() {
        var viewContainer = $('[data-role="products-view"]');
        var viewTrigger = $('[data-role="products-view-trigger"]');

        viewContainer.hide();
        viewContainer.filter(':first').show();

        viewTrigger.click(function() {
            typeView = $(this).data('view');
            viewContainer.hide();
            viewContainer.filter(function() {
                return $(this).data('view') === typeView;
            }).fadeIn();
            viewTrigger.find('.filter').removeClass('active');
            $(this).find('.filter').addClass('active');
            return false;
        }).filter(':first').click();
    }

    function productFiltersShow() {
        var viewContainer = $('[data-role="filters-block"]');
        var viewTrigger = $('[data-role="filters-trigger"]');

        viewTrigger.click(function() {
            classCheck($(this) ,'active');
            classCheck(viewContainer, 'state');
        });
    }

    function filtersItems() {
        var filterItem = $('[data-role="filter-item"]');
        var filterItemToggle = $('[data-role="filter-item-toggle"]');
        filterItem.click(function() {
            filterItem.removeClass('active');
            $(this).addClass('active');
        });
        filterItemToggle.click(function() {
            $(this).toggleClass('active');
        });
    }

    // Tempory Order Steps show/hide
    function OrderSteps() {
        var decrLine = $('[data-role="decor-line"]');
        var decorDisk = decrLine.find('[data-role^="decor-disk-"]');
        var orderForm = $('[data-role="order-form"]');
        var formSteps = orderForm.find('[data-role^="order-step-"]');
        var next = $('[data-trigger="next"]');
        var prev = $('[data-trigger="prev"]');
        var finish = $('[data-trigger="finish"]');
        var index = 0;

        finish.hide();
        prev.hide();

        function setCurrentItems(itemsArray, decorArray, action) {

            for (i = 0; i < itemsArray.length; i++) {
                var item = itemsArray.eq(i);
                var decorItem = decorArray.eq(i)
                if (item.hasClass('active')) {
                    item.removeClass('active');
                    item.hide();
                    if (action == 'next') {
                        index = itemsArray.index(item) + 1;
                    } else if (action == 'prev') {
                        index = itemsArray.index(item) - 1;
                        decorItem.removeClass('active');
                    }
                }
            }

            // item active
            newItem = itemsArray.eq(index);
            newItem.fadeIn().addClass('active');

            // decor item active
            newDecorArray = decorArray.eq(index);
            newDecorArray.addClass('active');

            if (itemsArray.eq(0).hasClass('active')) {
                prev.hide();
            } else {
                prev.show();
            }
            if (itemsArray.eq(itemsArray.length-1).hasClass('active')) {
                next.hide();
                finish.show();
            } else {
                next.show();
                finish.hide();
            }
        }

        // next function
        next.click(function() {
            setCurrentItems(formSteps, decorDisk, 'next');
        });

        // prev function
        prev.click(function() {
            setCurrentItems(formSteps, decorDisk, 'prev');
        });
    }

    // ProductChars
    function ProductChars() {
        var viewContainer = $('[data-role="products-chars"]');
        var viewTrigger = $('[data-role="products-chars-trigger"]');

        viewContainer.hide();
        viewContainer.filter(':first').show();

        viewTrigger.click(function() {
            typeView = $(this).data('view');
            viewContainer.hide();
            viewContainer.filter(function() {
                return $(this).data('view') === typeView;
            }).fadeIn();
            viewTrigger.removeClass('active');
            $(this).addClass('active');
            return false;
        }).filter(':first').click();
    }

    // ProductImage
    function ProductImage() {
        var viewImage = $('[data-role="product-image"]');
        var viewTrigger = $('[data-role="product-image-trigger"]');

        viewImage.hide();
        viewImage.filter(':first').show();

        viewTrigger.click(function() {
            typeView = $(this).data('image');
            viewImage.hide();
            viewImage.filter(function() {
                return $(this).data('image') === typeView;
            }).fadeIn();
            viewTrigger.removeClass('active');
            $(this).addClass('active');
            return false;
        }).filter(':first').click();
    }

    function CartDisplay() {

        var cartDisplay = $('[data-role="cart-display"]');
        var cartTrigger = $('[data-role="cart-display-trigger"]');
        var cartTriggerMobile = $('[data-role="cart-display-trigger-mobile"]');
        var cartTriggerCount = $('[data-role="cart-display-trigger-count"]');
        var mainHeader = $('[data-role="main-header"]');

        triggerHeight = cartTrigger.height();
        triggerWidth = cartTrigger.width();

        triggerPosition = cartTrigger.position();

        cartDisplayWidth = cartDisplay.width();

        // position & styles
        if (window.matchMedia('(min-width : 768px)').matches) {

            topForCartDisplay = (triggerHeight + triggerPosition.top + 20);
            leftForCartDisplay = (triggerPosition.left + triggerWidth)
            cartDisplay.removeAttr('style');
            cartDisplay.css({
                'top': topForCartDisplay,
                'left': leftForCartDisplay,
                'margin-left': -(cartDisplayWidth),
            });
        } else {
            cartDisplay.removeAttr('style');
            cartDisplay.css({
                'top': mainHeader.outerHeight()
            });
        }

        // Behavior
        cartTrigger.click(function() {
            classCheck(cartDisplay, 'opened');
            classCheck(cartTriggerMobile, 'active');
            classCheck($(this), 'active');
        });

        cartTriggerMobile.click(function() {
            classCheck(cartDisplay, 'opened');
            classCheck(cartTrigger, 'active');
            classCheck($(this), 'active');
        });
    }

    // Cart behavior
    // Count items
    function cartItemCountUpdate() {
        var item = $('[data-role="cart-item"]')

        item.each(function() {
            var input = $(this).find('[data-role="cart-item-count"]');
            var plus = $(this).find('[data-role="cart-item-count-plus"]');
            var minus = $(this).find('[data-role="cart-item-count-minus"]');
            var itemDelete = $(this).find('[data-role="cart-item-count-delete"]');

            minus.hide();
            itemDelete.show();

            plus.click(function() {
                var inputValue = parseInt(input.val());
                function update() {
                    inputValueUpdated = parseInt((inputValue + 1))
                    if (inputValueUpdated > 1) {
                        minus.show();
                        itemDelete.hide();
                    }
                }
                update();
                input.val(inputValueUpdated);
            });
            minus.click(function() {
                inputValue = parseInt(input.val());
                function update() {
                    inputValueUpdated = parseInt((inputValue - 1))
                    if (inputValueUpdated === 1) {
                        minus.hide();
                        itemDelete.show();
                    }
                }
                update();
                input.val(inputValueUpdated);
            });
        });
    }
    // Show/hide oneclick install
    function oneClickOrder() {
        var cartDisplay = $('[data-role="cart-items"]');
        var orderDisplay = $('[data-role="cart-order"]');
        var trigger = $('[data-role="trigger-one-click"]');
        var triggerHide = $('[data-role="trigger-one-click-hide"]');

        trigger.click(function() {
            cartDisplay.hide();
            orderDisplay.fadeIn();
        });
        triggerHide.click(function() {
            orderDisplay.hide();
            cartDisplay.fadeIn();
        });
    }

    // phone mask
    function phoneMask() {
        var phoneInput = $('[data-role="phone-mask"]');
        phoneInput.mask("(000) 000-00-00", {placeholder: "(099) 999-99-99"});
    }

    // popup menu
    function popupSearch() {
        var search = $('[data-role="popup-search"]');
        var searchTrigger = $('[data-role="popup-search-trigger"]');
        var productMenu = $('[data-role="product-menu"]');

        productPosition = productMenu.position();
        popupTop = productPosition.top + productMenu.outerHeight();

        search.css('top', popupTop);
        classCheckByTrigger(search, searchTrigger, 'active');
    }

    function productSubMenu() {
        var menu = $('[data-role="product-menu"]');
        var subMenu = $('[data-role="product-submenu"]');
        subMenu.css('top', menu.height());
    }

    // popup menu
    function popupMenu() {
        var menu = $('[data-role="popup-menu"]');
        var menuTrigger = $('[data-role="popup-menu-trigger"]');
        var productMenu = $('[data-role="product-menu"]');

        productPosition = productMenu.position();
        popupTop = productPosition.top + productMenu.outerHeight();

        menu.css('top', popupTop);
        classCheckByTrigger(menu, menuTrigger, 'active');
    }

    function popupMobileMenu() {
        var menu = $('[data-role="popup-mobile-menu"]');
        var menuTrigger = $('[data-role="popup-mobile-menu-trigger"]');
        var header = $('[data-role="main-header"]');

        headerPosition = header.position();
        popupTop = headerPosition.top + header.outerHeight();
        menu.css('top', popupTop);
        classCheckByTrigger(menu, menuTrigger, 'active');
    }

    function disabledElement() {
        var elem = $('[data-role="disabled"]');
        elem.off();
    }

    // // Price range slider
    // function priceRange(sliderid, min, max, values) {

    //     function collision($div1, $div2) {
    //         var x1 = $div1.offset().left;
    //         var w1 = 40;
    //         var r1 = x1 + w1;
    //         var x2 = $div2.offset().left;
    //         var w2 = 40;
    //         var r2 = x2 + w2;

    //         if (r1 < x2 || x1 > r2) return false;
    //         return true;

    //     }

    //     function updateFromInputMin() {
    //         $('[data-role="field-min"]').keyup(function(e) {
    //             oldMax = $('#' + sliderid).slider('values', 1 );
    //             newMin = $(this).val();
    //             $('#' + sliderid).slider("option", "values", [newMin, oldMax]);
    //             updateMin(newMin);
    //             updateDiffLine(newMin, oldMax);
    //         });
    //     }

    //     function updateFromInputMax() {
    //         $('[data-role="field-max"]').keyup(function() {
    //             oldMin = $('#' + sliderid).slider('values', 0 );
    //             newMax = $(this).val();
    //             $('#' + sliderid).slider("option", "values", [oldMin, newMax]);
    //             updateMax(newMax);
    //             updateDiffLine(oldMin, newMax);
    //         });
    //     }

    //     function updateBothValues(currenValMin, currenValMax) {
    //         $('[data-role="field-min"]').attr('value', currenValMin);
    //         $('[data-role="field-max"]').attr('value', currenValMax);
    //         updateDiffLine(currenValMin, currenValMax);
    //     }

    //     function updateMax(currentValueMax) {
    //         $('.ui-slider-range').find('span.price-range-both')
    //         .attr('data-highprice', currentValueMax);
    //         $('.ui-slider-handle:eq(1)').html('<span class="price-range-max value">'
    //         + currentValueMax + ' грн</span>');
    //     }
    //     function updateMin(currentValueMin) {
    //         $('.ui-slider-range').find('span.price-range-both')
    //         .attr('data-highprice', currentValueMin);
    //         $('.ui-slider-handle:eq(0)').html('<span class="price-range-min value">'
    //         + currentValueMin + ' грн</span>');
    //     }

    //     function updateDiffLine(currentValueMin, currentValueMax) {
    //         $('.ui-slider-range').html('<span class="price-range-both value"><i>'
    //         + currentValueMin + ' грн - ' + currentValueMax + ' грн</i></span>');
    //         $('#range-both').html('<span class="price-range-both value">' + currentValueMin +
    //             ' - ' + currentValueMax + '</span>');
    //     }

    //     $('#' + sliderid).slider({
    //         range: true,
    //         min: min,
    //         max: max,
    //         values: values,
    //         slide: function(event, ui) {

    //             $('[data-role="field-min"]').attr('value', ui.values[ 0 ]);
    //             $('[data-role="field-max"]').attr('value', ui.values[ 1 ]);

    //             $('.ui-slider-handle:eq(0) .price-range-min').html(ui.values[ 0 ] + ' грн');
    //             $('.ui-slider-handle:eq(1) .price-range-max').html(ui.values[ 1 ] + ' грн');
    //             $('.price-range-both').html('<i>' + ui.values[ 0 ] + ' грн - ' + ui.values[ 1 ] + ' грн</i>');
    //             $('.ui-slider-range').find('span.price-range-both').attr('data-lowprice', ui.values[ 0 ]);
    //             $('.ui-slider-range').find('span.price-range-both').attr('data-highprice', ui.values[ 1 ]);
    //             $('#range-both').html(ui.values[ 0 ] + ' - ' + ui.values[ 1 ]);

    //             updateBothValues(ui.values[ 0 ], ui.values[ 1 ]);

    //             if (collision($('.price-range-min'), $('.price-range-max')) === true) {
    //                 $('.price-range-min, .price-range-max').css('opacity', '0');
    //             } else {
    //                 $('.price-range-min, .price-range-max').css('opacity', '1');
    //             }

    //         }
    //     });

    //     valueMin = $('#' + sliderid).slider('values', 0 );
    //     valueMax = $('#' + sliderid).slider('values', 1 );

    //     updateMin(valueMin);
    //     updateMax(valueMax);
    //     updateBothValues(valueMin, valueMax);
    //     updateFromInputMin();
    //     updateFromInputMax();
    // }

    function slickStandart(argContainer, argBaner, argPrev, argNext) {
        var banerContainer = argContainer;
        var banerSelector = argBaner;
        var prev = argPrev;
        var next = argNext;

        banerContainer.slick({
            infinite: true,
            slidesToShow: 1,
            slidesToScroll: 1,
            slide: banerSelector,
            arrows: false,
            autoplay: true,
            autoplaySpeed: 5000,
        });
        if(next != null) {
            next.click(function(e){
                banerContainer.slick('slickNext');
                console.log('yay');
            });
        }
        if(prev != null) {
            prev.click(function(e){
                banerContainer.slick('slickPrev');
                console.log('fof');
            });
        }
    }

    function topBanners() {
        slickStandart(
                $('[data-role="main-baners"]'),
                '[data-role="main-baner"]', // this is string – this requirement
                $('[data-role="baner-prev"]'),
                $('[data-role="baner-next"]')
        );
        slickStandart(
                $('[data-role="top-baners"]'),
                '[data-role="top-baner"]', // this is string – this requirement
                null,
                null
        );
        slickStandart(
                $('[data-role="sub-images"]'),
                '[data-role="sub-image"]', // this is string – this requirement
                null,
                $('[data-role="sub-image-next"]')
        );
    }

    function galleryDisplay() {
        var galleryItem = $('[data-role="gallery-item"]');

        galleryItem.each(function() {
            var expand = $(this).find('[data-role="gallery-expand"]');
            var expandTrigger = $(this).find('[data-trigger="gallery-expand-trigger"]');
            var overlay = $(this).find('[data-role="gallery-overlay"]');
            var close = $(this).find('[data-role="close"]');

            expandTrigger.click(function() {
                overlay.toggleClass('active');
                expand.toggleClass('active');
                $('body').toggleClass('open-gallery');
            });

            close.click(function() {
                overlay.removeClass('active');
                expand.removeClass('active');
                $('body').removeClass('open-gallery');
            });

            $(document).keyup(function(e) {
                if (e.keyCode == 27) {
                    overlay.removeClass('active');
                    expand.removeClass('active');
                    $('body').removeClass('open-gallery');
                }
            });
        });
    }

    // document ready
    $(window).on('load', function() {
        topBanners();
        ProductsViewType();
        OrderSteps();
        ProductChars();
        ProductImage();
        cartItemCountUpdate();
        oneClickOrder();
        phoneMask();
        CartDisplay();
        productFiltersShow();
        filtersItems();
        priceRange('price', 0, 1000, [10, 500]);
        Tabs();
        popupSearch();
        productSubMenu();
        popupMenu();
        popupMobileMenu();
        disabledElement();
        galleryDisplay();
    });

    // all initial on window resize
    $(window).on('resize', function() {
        CartDisplay();
    });


})(jQuery);
