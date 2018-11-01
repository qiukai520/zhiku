

          // 根据城市获取相应的县区
    function SelectCountry(ths) {
      var nid=$(ths).val();
      $("#town_id").children().remove();
      $.ajax({
        url:"country_town",
        type:'get',
        data:{"id":nid},
        dataType:'json',
        async: true,//是否异步
        success: function (arg) {
	    var objs = JSON.parse(arg.data);
	     $("#town_id").append("<option value=0 >请选择街道</option>")
	    $(objs).each(function () {
		var o = document.createElement("option");
		o.value = this['pk'];
		o.text = this['fields']['town'];
		 $("#town_id").append(o);
	  });
	},
        error: function (arg) {
          alert(arg.message);
        },
    });
    }
        // 根据省份获取相应的城市
    function SelectCity(ths) {
      var nid=$(ths).val();
      $("#country").children().remove();
      $.ajax({
        url:"city_country",
        type:'get',
        data:{"id":nid},
        dataType:'json',
        async: true,//是否异步
        success: function (arg) {
	    var objs = JSON.parse(arg.data);
	    $("#country").append("<option value=0 >请选择县区</option>")
	    $(objs).each(function () {
		var o = document.createElement("option");
		o.value = this['pk'];
		o.text = this['fields']['country'];
		 $("#country").append(o);
	  });
	},
        error: function (arg) {
          alert(arg.message);
        },
    });
    }

    // 根据省份获取相应的城市
    function SelectProvince(ths) {
      var nid=$(ths).val();
      $("#city").empty();
      $("#country").empty();
      $("#town_id").empty();
      $.ajax({
        url:"province_city",
        type:'get',
        data:{"id":nid},
        dataType:'json',
        async: true,//是否异步
        success: function (arg) {
	    var objs = JSON.parse(arg.data);
	    $("#city").append("<option value=0 >请选择城市</option>")
	    $(objs).each(function () {
		var o = document.createElement("option");
		o.value = this['pk'];
		o.text = this['fields']['city'];
		 $("#city").append(o);
	  });
	},
        error: function (arg) {
          alert(arg.message);
        },
    });
    }