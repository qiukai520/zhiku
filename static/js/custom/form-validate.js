$.validator.setDefaults({
    highlight:function(e){$(e).closest(".form-group").removeClass("has-success").addClass("has-error")},
    success:function(e){e.closest(".form-group").removeClass("has-error").addClass("has-success")},
    errorElement:"span",
    errorPlacement:function(e,r){e.appendTo(r.is(":radio")||r.is(":checkbox")?r.parent().parent().parent():r.parent())},
    errorClass:"help-block m-b-none",
    validClass:"help-block m-b-none"
}),
    $().ready(function(){
        var e="<i class='fa fa-times-circle'></i> ";
        $("#fm").validate({
            focusInvalid :true,//当验证无效时，焦点跳到第一个无效的表单元素,
            //(但是只有当表单提交发生时它才有效。 如果用 valid 方法验证表单，则它不起作用)
            // 解决办法，使用invalidHandler 方法
            onfocusout: false,
            rules:{
                job_number:"required",
                name: {
                        required: true,
                        maxlength: 16
                      },
                phone: {
                        required: true,
                        rangelength:[11,11]
                      },
                id_card:{
                        required: true,
                        rangelength: [15,18]
                      },
                // email:{
                //     required:false,email:true
                // },
                birthday:{
                    required:false,date:true
                },
                 contact_phone: {
                        required: false,
                        rangelength:[11,11]
                      },

                // username:{required:!0,minlength:2},
                // password:{required:!0,minlength:5},
                // confirm_password:{required:!0,minlength:5,equalTo:"#password"},
                // email:{required:!0,email:!0},
                // topic:{required:"#newsletter:checked",minlength:2},
                // agree:"required"
            },
            messages: {
                job_number:e+"请输入工号",
                name: {
                    required: e+"请输入姓名",
                    maxlength: e+"姓名长度不能超过十六个字符"
                },
                phone:{
                    required: e+"手机号不能为空",
                    rangelength: e+"手机号长度不能超过或低于11位"
                },
                id_card:{
                    required: e+"身份证不能为空",
                    rangelength: e+"身份证号长度应在15-18位之间"
                },
                email:e+"请输入合法的E-mail",
                birthday: e+"请输入合法日期",
                contact_phone:{
                    rangelength: e+"手机号长度不能超过或低于11位"
                },

                // username:{required:e+"请输入您的用户名",minlength:e+"用户名必须两个字符以上"},
                // password:{required:e+"请输入您的密码",minlength:e+"密码必须5个字符以上"},
                // confirm_password:{required:e+"请再次输入密码",minlength:e+"密码必须5个字符以上",equalTo:e+"两次输入的密码不一致"},
                // email:e+"请输入您的E-mail",
                // agree:{required:e+"必须同意协议后才能注册",element:"#agree-error"}
            },
            invalidHandler: function(form, validator) {
                var errors = validator.numberOfInvalids();
                if (errors) {
                    validator.errorList[0].element.focus();
                }
            }
            });
        $("#price_fm").validate({
            focusInvalid :true,//当验证无效时，焦点跳到第一个无效的表单元素,
            //(但是只有当表单提交发生时它才有效。 如果用 valid 方法验证表单，则它不起作用)
            // 解决办法，使用invalidHandler 方法
            onfocusout: false,
            rules:{
                amount: {
                        required: true,
                      },
                logistics: {
                        required: true,
                      },
                supplier_id:{
                 required: true,
                 min:1,
                 digits: true,
                     },
               linkman_id:{
                 required: true,
                 min:1,
                 digits: true,
              },
                // username:{required:!0,minlength:2},
                // password:{required:!0,minlength:5},
                // confirm_password:{required:!0,minlength:5,equalTo:"#password"},
                // email:{required:!0,email:!0},
                // topic:{required:"#newsletter:checked",minlength:2},
                // agree:"required"
            },
            messages: {
                amount: {
                    required: e+"请输入数量",
                    digits: e+"请输入有效的整数"
                },
                supplier_id:{
                    required:"请选择供应商",
                    digits:"请选择供应商",
                    min:"请选择供应商"
                },
                linkman_id:{
                    required:"请选择联系人",
                    digits:"请选择联系人",
                    min:"请选择联系人"
                },
                 logistics:{
                    required: e+"物流价格不能为空",
                },

                // username:{required:e+"请输入您的用户名",minlength:e+"用户名必须两个字符以上"},
                // password:{required:e+"请输入您的密码",minlength:e+"密码必须5个字符以上"},
                // confirm_password:{required:e+"请再次输入密码",minlength:e+"密码必须5个字符以上",equalTo:e+"两次输入的密码不一致"},
                // email:e+"请输入您的E-mail",
                // agree:{required:e+"必须同意协议后才能注册",element:"#agree-error"}
            },
            invalidHandler: function(form, validator) {
                var errors = validator.numberOfInvalids();
                if (errors) {
                    validator.errorList[0].element.focus();
                }
            }
            });
        $("#good_fm").validate({
            focusInvalid :true,//当验证无效时，焦点跳到第一个无效的表单元素,
            //(但是只有当表单提交发生时它才有效。 如果用 valid 方法验证表单，则它不起作用)
            // 解决办法，使用invalidHandler 方法
            onfocusout: false,
            rules:{
                name: {
                        required: true,
                        maxlength: 16
                      },
                start_month: {
                            required: true,
                            digits: true
                        },
                end_month: {
                            required: true,
                            digits: true
                        },
            },
            messages: {
                name: {
                    required: e+"请输入商品名称",
                },
                start_month: {
                            required: "开始月份不可以为空",
                            digits: "请输入整数"
                        },
                end_month: {
                            required: "结束月份不可以为空",
                            digits: "请输入整数"
                        }

                // username:{required:e+"请输入您的用户名",minlength:e+"用户名必须两个字符以上"},
                // password:{required:e+"请输入您的密码",minlength:e+"密码必须5个字符以上"},
                // confirm_password:{required:e+"请再次输入密码",minlength:e+"密码必须5个字符以上",equalTo:e+"两次输入的密码不一致"},
                // email:e+"请输入您的E-mail",
                // agree:{required:e+"必须同意协议后才能注册",element:"#agree-error"}
            },
            invalidHandler: function(form, validator) {
                var errors = validator.numberOfInvalids();
                if (errors) {
                    validator.errorList[0].element.focus();
                }
            }
            });
        $("#supplier_fm").validate({
            focusInvalid :true,//当验证无效时，焦点跳到第一个无效的表单元素,
            //(但是只有当表单提交发生时它才有效。 如果用 valid 方法验证表单，则它不起作用)
            // 解决办法，使用invalidHandler 方法
            onfocusout: false,
            rules:{
                company: {
                        required: true,
                        maxlength: 32
                      },
                business: {
                        required: true,
                        maxlength: 32
                      },
               town_id:{
                     required: true,
                     min:1,
                     digits: true,
                },
            },
            messages: {
                town_id:{
                    required:"请选择街道",
                    digits:"请选择街道",
                    min:"请选择街道"
                },
                company: {
                    required: e+"请输入公司名称",
                },
                 business: {
                    required: e+"主营业务不能为空",
                },
                // username:{required:e+"请输入您的用户名",minlength:e+"用户名必须两个字符以上"},
                // password:{required:e+"请输入您的密码",minlength:e+"密码必须5个字符以上"},
                // confirm_password:{required:e+"请再次输入密码",minlength:e+"密码必须5个字符以上",equalTo:e+"两次输入的密码不一致"},
                // email:e+"请输入您的E-mail",
                // agree:{required:e+"必须同意协议后才能注册",element:"#agree-error"}
            },
            invalidHandler: function(form, validator) {
                var errors = validator.numberOfInvalids();
                if (errors) {
                    validator.errorList[0].element.focus();
                }
            }
            });
        $("#contact_fm").validate({
            focusInvalid :true,//当验证无效时，焦点跳到第一个无效的表单元素,
            //(但是只有当表单提交发生时它才有效。 如果用 valid 方法验证表单，则它不起作用)
            // 解决办法，使用invalidHandler 方法
            onfocusout: false,
            rules:{
                description: {
                        required: true,
                        maxlength: 128
                      },
                date: {
                        required: true,
                        },
                project:{
                      required: true,
                },
                category_id:"required",
                linkman_id:"required",
            },
            messages: {
                category_id:e+"请选择联系人",
                category:e+"请选择交易类别",
                description: {
                    required: e+"请输入商品名称",
                    maxlength:e+"项目描述不能超过128个字符"
                },
                 project: {
                    required: e+"请输入项目名称",
                },
                  date: {
                            required: "请输入日期",
                            date: "请输入正确的日期格式"
                        }
                // username:{required:e+"请输入您的用户名",minlength:e+"用户名必须两个字符以上"},
                // password:{required:e+"请输入您的密码",minlength:e+"密码必须5个字符以上"},
                // confirm_password:{required:e+"请再次输入密码",minlength:e+"密码必须5个字符以上",equalTo:e+"两次输入的密码不一致"},
                // email:e+"请输入您的E-mail",
                // agree:{required:e+"必须同意协议后才能注册",element:"#agree-error"}
            },
            invalidHandler: function(form, validator) {
                var errors = validator.numberOfInvalids();
                if (errors) {
                    validator.errorList[0].element.focus();
                }
            }
            });
        $("#linkman_fm").validate({
            focusInvalid :true,//当验证无效时，焦点跳到第一个无效的表单元素,
            //(但是只有当表单提交发生时它才有效。 如果用 valid 方法验证表单，则它不起作用)
            // 解决办法，使用invalidHandler 方法
            onfocusout: false,
            rules:{
                name: {
                        required: true,
                        maxlength:16
                      },
                birthday: {
                        required: true,
                        },
                phone:{
                      required: true,
                },
            },
            messages: {
                name: {
                    required: e+"姓名不能为空",
                    maxlength:e+"姓名长度不能超过16个字符"
                },
                birthday: {
                            required: "请输入生日日期",
                            date: "请输入正确的日期格式"
                },
                phone:{
                     required:"请输入电话号码"
                },


                // username:{required:e+"请输入您的用户名",minlength:e+"用户名必须两个字符以上"},
                // password:{required:e+"请输入您的密码",minlength:e+"密码必须5个字符以上"},
                // confirm_password:{required:e+"请再次输入密码",minlength:e+"密码必须5个字符以上",equalTo:e+"两次输入的密码不一致"},
                // email:e+"请输入您的E-mail",
                // agree:{required:e+"必须同意协议后才能注册",element:"#agree-error"}
            },
            invalidHandler: function(form, validator) {
                var errors = validator.numberOfInvalids();
                if (errors) {
                    validator.errorList[0].element.focus();
                }
            }
            });
        $("#memo_fm").validate({
            focusInvalid :true,//当验证无效时，焦点跳到第一个无效的表单元素,
            //(但是只有当表单提交发生时它才有效。 如果用 valid 方法验证表单，则它不起作用)
            // 解决办法，使用invalidHandler 方法
            onfocusout: false,
            rules:{
                title: {
                        required: true,
                        maxlength: 128
                      },
                detail: {
                        required: true,
                        maxlength: 512
                      },
            },
            messages: {
                title: {
                    required: e+"请输入标题",
                    maxlength:e+"标题不能超过128个字符"
                },
                 detail: {
                    required: e+"请输入详细",
                    maxlength:e+"详细不能超过128个字符"
                },
                // username:{required:e+"请输入您的用户名",minlength:e+"用户名必须两个字符以上"},
                // password:{required:e+"请输入您的密码",minlength:e+"密码必须5个字符以上"},
                // confirm_password:{required:e+"请再次输入密码",minlength:e+"密码必须5个字符以上",equalTo:e+"两次输入的密码不一致"},
                // email:e+"请输入您的E-mail",
                // agree:{required:e+"必须同意协议后才能注册",element:"#agree-error"}
            },
            invalidHandler: function(form, validator) {
                var errors = validator.numberOfInvalids();
                if (errors) {
                    validator.errorList[0].element.focus();
                }
            }
            });
        $("#warehouse_fm").validate({
            focusInvalid :true,//当验证无效时，焦点跳到第一个无效的表单元素,
            //(但是只有当表单提交发生时它才有效。 如果用 valid 方法验证表单，则它不起作用)
            // 解决办法，使用invalidHandler 方法
            onfocusout: false,
            rules:{
                name: {
                        required: true,
                        maxlength: 64
                      },
                town_id:{
                     required: true,
                     digits: true,
                     min:1
                },
                lng:{
                    required:true,
                },
                lat:{
                    required:true,
                },
                address: {
                        required: true,
                        maxlength: 128
                      },

            },
            messages: {
                town_id:{
                    required:"请选择街道",
                    digits:"请选择街道",
                    min:"请选择街道"
                },
                name: {
                    required: "请输入商品名称",
                },
                address:{
                     required: "请输入详细地址",
                     maxlength: "地址不能超过128个字符"
                },
                lng:e+"请选择定位",
                lat:e+"请选择定位",

                // username:{required:e+"请输入您的用户名",minlength:e+"用户名必须两个字符以上"},
                // password:{required:e+"请输入您的密码",minlength:e+"密码必须5个字符以上"},
                // confirm_password:{required:e+"请再次输入密码",minlength:e+"密码必须5个字符以上",equalTo:e+"两次输入的密码不一致"},
                // email:e+"请输入您的E-mail",
                // agree:{required:e+"必须同意协议后才能注册",element:"#agree-error"}
            },
            invalidHandler: function(form, validator) {
                var errors = validator.numberOfInvalids();
                if (errors) {
                    validator.errorList[0].element.focus();
                }
            }
            });
        $("#customer_fm").validate({
            focusInvalid :true,//当验证无效时，焦点跳到第一个无效的表单元素,
            //(但是只有当表单提交发生时它才有效。 如果用 valid 方法验证表单，则它不起作用)
            // 解决办法，使用invalidHandler 方法
            onfocusout: false,
            rules:{
                company: {
                        required: true,
                        maxlength: 32
                      },
                country_id:"required",
            },
            messages: {
                country_id:e+"请选择县（区）",
                company: {
                    required: e+"请输入公司名称",
                },
                // username:{required:e+"请输入您的用户名",minlength:e+"用户名必须两个字符以上"},
                // password:{required:e+"请输入您的密码",minlength:e+"密码必须5个字符以上"},
                // confirm_password:{required:e+"请再次输入密码",minlength:e+"密码必须5个字符以上",equalTo:e+"两次输入的密码不一致"},
                // email:e+"请输入您的E-mail",
                // agree:{required:e+"必须同意协议后才能注册",element:"#agree-error"}
            },
            invalidHandler: function(form, validator) {
                var errors = validator.numberOfInvalids();
                if (errors) {
                    validator.errorList[0].element.focus();
                }
            }
            });
        $("#invent_fm").validate({
            focusInvalid :true,//当验证无效时，焦点跳到第一个无效的表单元素,
            //(但是只有当表单提交发生时它才有效。 如果用 valid 方法验证表单，则它不起作用)
            // 解决办法，使用invalidHandler 方法
            onfocusout: false,
            rules:{
                amount: {
                        required: true,
                      },
                location_id:{
                     required: true,
                     digits: true,
                     min:1
                },
                  date: {
                        required: true,
                        date:true
                        },

            },
            messages: {
                location_id:{
                    required:"请选择库位",
                    digits:"请选择库位",
                    min:"请选择库位"
                },
                amount: {
                    required: "请输入入库数量",
                },
                 date: {
                    required: "请输入日期",
                     date:"请输入正确的日期格式",
                },

                // username:{required:e+"请输入您的用户名",minlength:e+"用户名必须两个字符以上"},
                // password:{required:e+"请输入您的密码",minlength:e+"密码必须5个字符以上"},
                // confirm_password:{required:e+"请再次输入密码",minlength:e+"密码必须5个字符以上",equalTo:e+"两次输入的密码不一致"},
                // email:e+"请输入您的E-mail",
                // agree:{required:e+"必须同意协议后才能注册",element:"#agree-error"}
            },
            invalidHandler: function(form, validator) {
                var errors = validator.numberOfInvalids();
                if (errors) {
                    validator.errorList[0].element.focus();
                }
            }
            });
        $("#contract_fm").validate({
            focusInvalid :true,//当验证无效时，焦点跳到第一个无效的表单元素,
            //(但是只有当表单提交发生时它才有效。 如果用 valid 方法验证表单，则它不起作用)
            // 解决办法，使用invalidHandler 方法
            onfocusout: false,
            rules:{
                sign: {
                        required: true,
                        },
                start_date: {
                        required: true,
                        },
                end_date: {
                        required: true,
                        },
                number:{
                      required: true,
                },
                customer_id:"required",
                product_id:"required",
                product_meal_id:"required",
                receivable:"required",
            },
            messages: {
                customer_id:e+"请选择客户",
                product_id:e+"请选择签约产品",
                product_meal_id:e+"请选择产品套餐",
                number: {
                    required: e+"请输入合同编号",
                },
                receivable: {
                    required: e+"请输入应收金额",
                },
              sign: {
                        required: "请输入日期",
                        date: "请输入正确的日期格式"
                    },
                 start_date: {
                        required: "请输入日期",
                        date: "请输入正确的日期格式"
                    },
                 end_date: {
                        required: "请输入日期",
                        date: "请输入正确的日期格式"
                    },
                // username:{required:e+"请输入您的用户名",minlength:e+"用户名必须两个字符以上"},
                // password:{required:e+"请输入您的密码",minlength:e+"密码必须5个字符以上"},
                // confirm_password:{required:e+"请再次输入密码",minlength:e+"密码必须5个字符以上",equalTo:e+"两次输入的密码不一致"},
                // email:e+"请输入您的E-mail",
                // agree:{required:e+"必须同意协议后才能注册",element:"#agree-error"}
            },
            invalidHandler: function(form, validator) {
                var errors = validator.numberOfInvalids();
                if (errors) {
                    validator.errorList[0].element.focus();
                }
            }
            });
        $("#payment_fm").validate({
            focusInvalid :true,//当验证无效时，焦点跳到第一个无效的表单元素,
            //(但是只有当表单提交发生时它才有效。 如果用 valid 方法验证表单，则它不起作用)
            // 解决办法，使用invalidHandler 方法
            onfocusout: false,
            rules:{
                date: {
                        required: true,
                        },

            },
            messages: {
                 payment: {
                    required: e+"收款金额不能为空",
                },
              sign: {
                        required: "请输入日期",
                        date: "请输入正确的日期格式"
                    },
                // username:{required:e+"请输入您的用户名",minlength:e+"用户名必须两个字符以上"},
                // password:{required:e+"请输入您的密码",minlength:e+"密码必须5个字符以上"},
                // confirm_password:{required:e+"请再次输入密码",minlength:e+"密码必须5个字符以上",equalTo:e+"两次输入的密码不一致"},
                // email:e+"请输入您的E-mail",
                // agree:{required:e+"必须同意协议后才能注册",element:"#agree-error"}
            },
            invalidHandler: function(form, validator) {
                var errors = validator.numberOfInvalids();
                if (errors) {
                    validator.errorList[0].element.focus();
                }
            }
            });

    });
