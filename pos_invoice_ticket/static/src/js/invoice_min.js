openerp.pos_invoice_ticket = function(instance){
	var module = instance.point_of_sale;
	var Qweb = instance.web.qweb;
	var _t =    instance.web._t;

    var PosModelSuper = module.PosModel;
    module.PosModel = module.PosModel.extend({
        push_and_invoice_order: function(order){
            var self = this;
            var invoiced = PosModelSuper.prototype.push_and_invoice_order.call(this, order);
            return invoiced;
        },
    })

	module.PaymentScreenWidget.include({
        show: function(){
            var self = this;
            this._super();

            if(this.pos.config.iface_invoicing){
            	this.add_action_button({
                    label: _t('Invoice'),
                    name: 'invoice_ticket',
                    icon: '/pos_invoice_ticket/static/src/img/icons/png48/pdf.png',
                    click: function(){  
                        self.validate_order({invoice: true});
                    },
                });
            }
            this.update_payment_summary();

        },
        update_payment_summary: function() {
            var self = this;
            this._super();

            if(this.pos_widget.action_bar){
                this.pos_widget.action_bar.set_button_disabled('invoice_ticket', !this.is_paid());
            }
        },
        validate_order: function(options){
            var self = this;
            options = options || {};
            if(options.invoice_ticket){
                return
            }else{
                this._super(options);
            }
        }
    });

}