odoo.define('riyan_module.UserMenu', function (require) {
    "use strict";

    /**
     * This widget is appended by the webclient to the right of the navbar.
     * It displays the avatar and the name of the logged user (and optionally the
     * db name, in debug mode).
     * If clicked, it opens a dropdown allowing the user to perform actions like
     * editing its preferences, accessing the documentation, logging out...
     */
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var UserMenu = require('web.UserMenu');
    var documentation_url = 'http://www.greenit.com.np';
    var support_url = 'http://www.greenit.com.np';
    var account_title = 'My Account';
    var account_url = 'http://www.greenit.com.np';

    var QWeb = core.qweb;
    var _t = core._t;
    var _lt = core._lt;

    var map_title = {
        user_error: _lt('Warning'),
        warning: _lt('Warning'),
        access_error: _lt('Access Error'),
        missing_error: _lt('Missing Record'),
        validation_error: _lt('Validation Error'),
        except_orm: _lt('Global Business Error'),
        access_denied: _lt('Access Denied'),
    };

    UserMenu.include({
        init: function () {
            this._super.apply(this, arguments);
            var self = this;
            var session = this.getSession();

            
            self._rpc({
                model: 'ir.config_parameter',
                method: 'search_read',
                domain: [['key', '=like', 'gits_%']],
                fields: ['key', 'value'],
                lazy: false,
            }).then(function (res) {
                $.each(res, function (key, val) {
                    if (val.key == 'gits_documentation_url')
                        documentation_url = val.value;
                    if (val.key == 'gits_support_url')
                        support_url = val.value;
                    if (val.key == 'gits_account_title')
                        account_title = val.value;
                    if (val.key == 'gits_account_url')
                        account_url = val.value;
                    if (val.key == 'gits_show_documentation' && val.value == "False") {
                        $('[data-menu="documentation"]').hide();
                    }
                    if (val.key == 'gits_show_support' && val.value == "False") {
                        $('[data-menu="support"]').hide();
                    }
                    if (val.key == 'gits_show_account' && val.value == "False") {
                        $('[data-menu="account"]').hide();
                    }
                    if (val.key == 'gits_account_title' && val.value) {
                        $('[data-menu="account"]').html(account_title);
                    }
                    if (val.key == 'gits_show_poweredby' && val.value == "False") {
                        $('.o_sub_menu_footer').hide();
                    }
                });
            })
        },
        
        _onMenuAccount: function () {
            window.open(account_url, '_blank');
        },
        _onMenuDocumentation: function () {
            window.open(documentation_url, '_blank');
        },
        _onMenuSupport: function () {
            window.open(support_url, '_blank');
        },
    });

    Dialog.include({
        init: function (parent, options) {
            this._super(parent);
            this._opened = $.Deferred();
            // Normal Odoo dialogues have title Odoo followed by subtitle, Replace it
            options = _.defaults(options || {}, {
                title: _t(''), subtitle: '',
                size: 'large',
                dialogClass: '',
                $content: false,
                buttons: [{text: _t("Ok"), close: true}],
                technical: true,
            });

            this.$content = options.$content;
            this.title = options.title;
            this.subtitle = options.subtitle;
            this.dialogClass = options.dialogClass;
            this.size = options.size;
            this.buttons = options.buttons;
            this.technical = options.technical;
        },
    });
});
