// price input
function priceInput() {
    var item = $('[data-front="price-input"]')

    item.each(function() {
        var input = $(this).find('[data-front="price-input-count"]');
        var plus = $(this).find('[data-front="cart-input-count-plus"]');
        var minus = $(this).find('[data-front="cart-input-count-minus"]');

        plus.click(function() {
            var inputValue = parseInt(input.val());
            function update() {
                inputValueUpdated = parseInt((inputValue + 1));
            }
            update();
            input.val(inputValueUpdated);
            input.trigger('change');
        });
        minus.click(function() {
            inputValue = parseInt(input.val());
            function update() {
                inputValueUpdated = parseInt((inputValue - 1));
            }
            if (inputValue == 1 || inputValue < 0) {
                return false;
            } else {
                update();
                input.val(inputValueUpdated);
                input.trigger('change');
            }
        });
    });
}

// popup
function regularPopup() {
    var popup = $('[data-front="popup"]');
    var popupHeight = popup.height();
    var popupWidth = popup.width();
    popup.css({
        'left': '50%',
        'top': '50%',
        'position': 'fixed',
        'z-index': 9999,
        'margin-top': -popupHeight/2,
        'margin-left': -popupWidth/2
    });
}

(function($) {

    // functions
    function classCheck(elem, classname) {
        if (!elem.hasClass(classname)) {
            elem.addClass(classname);
        } else {
            elem.removeClass(classname);
        }
    }

    // equal height
    function equalheight(container) {

        var currentTallest = 0,
        currentRowStart = 0,
        rowDivs = new Array(),
        $el,
        topPosition = 0;

        $(container).each(function() {

            $el = $(this);
            $($el).height('auto')
            topPostion = $el.position().top;

            if (currentRowStart != topPostion) {
                for (currentDiv = 0 ; currentDiv < rowDivs.length ; currentDiv++) {
                    rowDivs[currentDiv].height(currentTallest);
                }
                rowDivs.length = 0; // empty the array
                currentRowStart = topPostion;
                currentTallest = $el.height();
                rowDivs.push($el);
            } else {
                rowDivs.push($el);
                currentTallest = (currentTallest < $el.height()) ? ($el.height()) : (currentTallest);
            }
            for (currentDiv = 0 ; currentDiv < rowDivs.length ; currentDiv++) {
                    rowDivs[currentDiv].height(currentTallest);
            }
        });
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

    // XXX: Duplicate: has to be moved to core
    // Read a page's GET URL variables and return them as an associative array.
    function getUrlVars()
    {
        if (window.location.href.indexOf('?') == -1) {
            return {};
        }
        var vars = [], hash;
        var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
        for(var i = 0; i < hashes.length; i++)
        {
            hash = hashes[i].split('=');
            vars[hash[0]] = hash[1];
        }
        return vars;
    }

    // XXX: Duplicate: has to be moved to core
    function setGetParameter(paramName, paramValue, url) {
        // returns current url with additional get parameter
        url = url || window.location.href;
        if (url.indexOf(paramName + '=') >= 0)
        {
            var prefix = url.substring(0, url.indexOf(paramName)),
            suffix = url.substring(url.indexOf(paramName));

            suffix = suffix.substring(suffix.indexOf('=') + 1);
            suffix = (suffix.indexOf('&') >= 0) ? suffix.substring(suffix.indexOf('&')) : '';
            url = prefix + paramName + '=' + paramValue + suffix;
        } else {
            if (url.indexOf('?') < 0) {
                url += '?' + paramName + '=' + paramValue;
            } else {
                url += '&' + paramName + '=' + paramValue;
            }
        }
        return url;
    }

    // ProductsViewType
    function ProductsViewType(viewIndex) {
        var viewContainer = $('[data-role="products-view"]');
        var viewTrigger = $('[data-role="products-view-trigger"]');
        var urlVars = getUrlVars();
        if (localStorage.view) {
            viewIndex = parseInt(localStorage.view, 10);
        }

        viewContainer.hide();
        viewContainer.filter(function(index) { return index === viewIndex; }).show();

        viewTrigger.click(function() {
            typeView = $(this).data('view');
            viewContainer.hide();
            viewContainer.filter(function() {
                return $(this).data('view') === typeView;
            }).fadeIn();
            viewTrigger.find('.filter').removeClass('active');
            $(this).find('.filter').addClass('active');
            return false;
        }).filter(function(index) { return index === viewIndex; }).click();

        viewContainer.click(function() {
            localStorage.view = 'grid';
        });

        $('[data-view="list"]').click(function() {localStorage.view = 1;});
        $('[data-view="grid"]').click(function() {localStorage.view = 0;});

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
        var filterItem = $('[front-role="filter-item"]');
        var filterItemToggle = $('[front-role="filter-item-toggle"]');
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
                var decorItem = decorArray.eq(i);
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
            leftForCartDisplay = (triggerPosition.left + triggerWidth);
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
        var wrap = menu.find('.wrap');
        var subMenu = $('[data-role="product-submenu"]');
        subMenu.css({
            'top': menu.height(),
            'width': wrap.width()
        });

        var subTabCont = $('[data-role="product-submenu"]');

        subTabCont.each(function() {
            var SubTabContainer = $(this).find('[data-role="sub-tab"]');
            var SubTabTrigger = $(this).find('[data-role="sub-tab-trigger"]');
            SubTabContainer.hide().filter(':first').show();
            SubTabTrigger.filter(':first').addClass('active');
            SubTabTrigger.hover(function () {
                var currentLoop = $(this).attr('sub-tabTrigger');
                SubTabContainer.hide();
                SubTabContainer.filter('[sub-tabTrigger='+currentLoop+']').show();
                SubTabTrigger.removeClass('active');
                $(this).addClass('active');
            });
        });
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
        if(next !== null) {
            next.click(function(e){
                banerContainer.slick('slickNext');
            });
        }
        if(prev !== null) {
            prev.click(function(e){
                banerContainer.slick('slickPrev');
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

    function addToCart() {
        $('.add-to-cart').click(function(event){
            return false;
        });
    }

    function reloadState() {
        $('[fron-state="reload-state"]').click(function() {
            location.reload();
        });
    }

    function sidePanel() {
        var marginDiffs = 370;
        var win = $(window);
        var sidePanel = $('[data-front="side-panel"]');
        if (sidePanel.length) {
            var offset = sidePanel.offset().top - marginDiffs;
        }
        var footer = $('.footer');
        var sidePanelHeight = sidePanel.height();
        var footerPosition = footer.offset().top - (sidePanel.height() + marginDiffs);


        if (window.matchMedia('(min-width : 768px)').matches) {
            win.scroll(function() {
                if (win.scrollTop() >= footerPosition) {
                    sidePanel.css({
                        "position": "absolute",
                        "top": 'auto',
                        "bottom": 0
                    });
                } else if (win.scrollTop() > offset) {
                    sidePanel.css({
                        "position": "fixed",
                        "top": 0,
                        "bottom": "auto"
                    });
                }
                else {
                    sidePanel.css({
                        "position": "static",
                        "top": 0,
                        "bottom": "auto"
                    });
                }
            });
        } else {
            sidePanel.css({
                "position": "static",
                "top": "auto",
                "bottom": "auto"
            });
        }
    }

    function sideScroll() {
        var scrollToTrigger = $('[data-front="scroll-to"]');

        scrollToTrigger.click(function() {
            var thisHash = this.hash;
            var scrollTo = null;
            if (thisHash == "#description" || !$(thisHash)) {
                scrollTo = 0 + "px";
            } else {
                scrollTo = $(thisHash).offset().top;
            }
            $('html, body').animate({
                scrollTop: scrollTo
            }, 300);
        });

        var win = $(window);
        var highLightItem = $('.product-block');
        var menuItem = $('.product-guides li a');

        win.scroll(function() {
            highLightItem.each(function() {
                if (win.scrollTop() >= $(this).offset().top -100) {
                    var highLightID = $(this).attr('id');
                    menuItem.removeClass('active');
                    menuItem.each(function() {
                        if ($(this).attr('href').split('#')[1] == highLightID) {
                            $(this).addClass('active');
                        }
                    });
                }
            });
        });

    }

    // tool tips
    // function toolTips() {
    //     var tipParent = $('[data-front="tooltip"]');

    //     tipParent.each(function() {
    //         var tip = $(this).find('[data-front="tooltip-display"]');
    //         // $(this).hover(function() {
    //             tip.css({
    //                 // 'top': -(tip.height() + 10),
    //                 // 'left': '50%'
    //                 // 'margin-left': 'x'
    //             });
    //         // });
    //     });
    // }

    // document ready
    $(window).on('load', function() {
        topBanners();
        ProductsViewType(1);
        OrderSteps();
        ProductChars();
        ProductImage();
        cartItemCountUpdate();
        oneClickOrder();
        phoneMask();
        CartDisplay();
        productFiltersShow();
        filtersItems();
        Tabs();
        popupSearch();
        productSubMenu();
        popupMenu();
        popupMobileMenu();
        disabledElement();
        galleryDisplay();
        addToCart();
        reloadState();
        sidePanel();
        sideScroll();
        priceInput();
        regularPopup();
        $('.products-view').css('display', 'block');
        // equalheight('[data-view="grid"] .products-list .product');

        $('[data-front="close-flash"]').click(function() {
            var flash = activateFlashPopUp();
            flash.deactivate();
        });
        if (localStorage.message) {
            var flash = activateFlashPopUp();
            flash.activate(localStorage.message);
            localStorage.removeItem("message");
        }
        $('[data-tooltip="tooltip"]').tooltipster({
            delay: 50,
            contentAsHTML: true,
            functionInit: function(origin, content) {
                content = origin.data('tip');
                return content;
            },
            theme: 'tooltipster-light'
        });
    });

    // all initial on window resize
    $(window).on('resize', function() {
        CartDisplay();
        sidePanel();
    });


})(jQuery);


/*

call this function with selector as argument, and after
use activate/deactivate

example

var newPop = activatePopUpBySelector('.newPop');
newPop.activate();
newPop.deactivate();

or

activatePopUpBySelector('.newPop').activate();

*/
function activatePopUpBySelector(selector) {
    var el = $(selector);
    return {
        activate: function() {
            el.addClass('active');
        },
        deactivate: function() {
            el.removeClass('active');
        }
    };
}

/*

activate flash message popup

var flash = activateFlashPopUp();
flash.activate('Some message');
flash.deactivate();

or

$('[data-front="close-flash"]').click(function() {
    flash.deactivate();
});

or other trigger

*/
function activateFlashPopUp() {
    var el = $('[data-front="flash-popup"]');
    var message = message;
    return {
        activate: function(message) {
            el.find('[data-front="message-content"]').html(message);
            el.addClass('active');
            setTimeout(function() {
                el.removeClass('active');
            }, 2500 * 3);
        },
        deactivate: function() {
            el.removeClass('active');
        }
    };
}
