

function Hidden(ths) {
      //隐藏当前标签
      $(ths).addClass("hide")

    }
    //字符串格式化
String.prototype.format=function()
{
  if(arguments.length==0) return this;
  for(var s=this, i=0; i<arguments.length; i++)
    s=s.replace(new RegExp("\\{"+i+"\\}","g"), arguments[i]);
  return s;
};



//添加附件
var att_num=1
//如果是修改的话，附件计数器设定为已存在的附件
function  AddAttachment (ths){
    if (att_num<=1){
        $(ths).parent().parent().find("label").text("附件1");
    }
    var tag = $(ths).parent().parent().parent().clone();
    att_num+=1
    $(tag).find("input").val("")
    $(tag).find("label").first().text("附件"+att_num);
    $(tag).find("button").remove()
    $(tag).find("input").first().parent().append();
    $(tag).find("input").first().parent().append('<button type="button" style="margin: 0px;" class="btn btn-danger inline "  onclick="RemoveAttachment(this)"><i  style ="" class="glyphicon glyphicon-minus minus "></i></button>\n'
);
    $(ths).parent().parent().parent().parent().append(tag);
}
//删除附件
function RemoveAttachment(ths){
    $(ths).parent().parent().parent().remove();
    att_num-=1
    var i=1
    $("#attachment-container").find('label[name="attach"]').each(function () {
        $(this).text("附件"+i)
        i+=1
    })
}
//清除任务附件标签
function clearAttachment(ths) {
    $(ths).parent().parent().parent().parent().remove()
    att_num-=1
}

