/**
 * 初始化duallistbox
 * reqeustParams：查询参数
 * selectElement：select元素对应属性
 * optionValue
 * optionText
 * selectedDataStr：选中数据，值以,隔开
 */
function initListBox(url,reqeustParams,selectElement,optionValue,optionText, selectedDataStr) {
  $.ajax({
	type: 'POST',//请求方式
	url: url,//地址，就是json文件的请求路径
	data: reqeustParams,//请求参数
	async: true,//是否异步
	success: function (data) {
	  var objs = $.parseJSON(data);
	  var selector = $(selectElement)[0];
	  $(objs).each(function () {
		var o = document.createElement("option");
		o.value = this[optionValue];
		o.text = this[optionText];
		if ("undefined" != typeof (selectedDataStr) && selectedDataStr != "") {
		  var selectedDataArray = selectedDataStr.split(',');
		  $.each(selectedDataArray, function (i, val) {
			if (o.value == val) {
			  o.selected = 'selected';
			  return false;
			}
		  });
		}
		if(typeof(selector) != "undefined") {
			selector.options.add(o);
		}
	  });

	  //渲染dualListbox
	     DualListboxObj = $(selectElement).bootstrapDualListbox({
		 nonSelectedListLabel: '可选',
         selectedListLabel: '已选',
         preserveSelectionOnMove: 'moved',
         moveOnSelect: false,
         infoTextEmpty: "",
         nonSelectedFilter: '',
         infoText:"数量:{0}"
	  });
	},
	error: function (e) {
	  alert(e.msg);
	}
  });
}
