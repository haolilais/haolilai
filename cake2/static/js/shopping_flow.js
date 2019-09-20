/* $Id : shopping_flow.js 4865 2007-01-31 14:04:10Z paulgao $ */

var selectedShipping = null;

var selectedshouhuo = null;

var selectedPayment  = null;
var selectedPack     = null;
var selectedCard     = null;
var selectedSurplus  = '';
var selectedBonus    = 0;
var selectedIntegral = 0;
var selectedOOS      = null;
var alertedSurplus   = false;

var groupBuyShipping = null;
var groupBuyPayment  = null;



var createAjax = function() {
    var xhr = null;
    try {
        //IE系列浏览器
        xhr = new ActiveXObject("microsoft.xmlhttp");
    } catch (e1) {
        try {
            //非IE浏览器
            xhr = new XMLHttpRequest();
        } catch (e2) {
            window.alert("您的浏览器不支持ajax，请更换！");
        }
    }
    return xhr;
};

var ajaxs = function(conf) {
    // 初始化
    //type参数,可选
    var type = conf.type;
    //url参数，必填 
    var url = conf.url;
    //data参数可选，只有在post请求时需要
    var data = conf.data;
    //datatype参数可选    
    var dataType = conf.dataType;
    //回调函数可选
    var success = conf.success;
                                                                                         
    if (type == null){
        //type参数可选，默认为get
        type = "get";
    }
    if (dataType == null){
        //dataType参数可选，默认为text
        dataType = "text";
    }
    // 创建ajax引擎对象
    var xhr = createAjax();
    // 打开
    xhr.open(type, url, true);
    // 发送
    if (type == "GET" || type == "get") {
        xhr.send(null);
    } else if (type == "POST" || type == "post") {
        xhr.setRequestHeader("content-type",
                    "application/x-www-form-urlencoded");
        xhr.send(data);
    }
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            if(dataType == "text"||dataType=="TEXT") {
                if (success != null){
                    //普通文本
                    success(xhr.responseText);
                }
            }else if(dataType=="xml"||dataType=="XML") {
                if (success != null){
                    //接收xml文档    
                    success(xhr.responseXML);
                }  
            }else if(dataType=="json"||dataType=="JSON") {
                if (success != null){
                    //将json字符串转换为js对象  
                    success(eval("("+xhr.responseText+")"));
                }
            }
        }
    };
};

/* *
 * 修改版改变发票的方式
 */
function changeNeedInv_muyu(type)
{

  if ($('input[name="add_finsh"]').val() == 0){
	layer.msg('请保存收货信息');
	return false;
  }
	
  var needInv    =  $(".fapiaos").is(":checked") ? 1 : 0;
	
  if(type==0){
	needInv= 0;
	$(".fapiaos").removeAttr("checked");
  }else{
	needInv = 1;
  }

  var invType    = $("input[name=inv_type]:checked").val();//类型
  var invContent   = $("#ECS_INVCONTENT").val();//内容
  var invPayee = $("#invTitle").val();//抬头

  if (!invType){
	  layer.msg("请填写发票类型",{time:2000});
	  return;
  }
  if (!invContent){
		layer.msg("请填写发票内容",{time:2000});
		return;
  }
  if(invType=='单位'){
	if(!invPayee){
		layer.msg("请填写单位名称",{time:2000});
		return;
	}
	var invNumber = $("#invNumber").val();//识别号
	var invMobile = $("#invMobile").val();//手机号
	var invEmail  = $("#invEmail").val();//邮箱
	if(!invNumber){
		layer.msg("请填写纳税人识别码",{time:2000});
		return;
	}
	if (!invMobile){
		layer.msg("请填写手机号",{time:2000});
		return;
	}else{
		var reg = /^1[3,2,4,6,5,7,8,9]\d{9}$/;
		if (!reg.test( invMobile )){
			layer.msg("手机号格式错误",{time:2000});
			return;
		}
	}
	if (!invEmail){
		layer.msg("请填写邮箱",{time:2000});
		return;
	}else{
		var reg = /([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)/
		if (!reg.test( invEmail )){
			layer.msg("邮箱格式错误",{time:2000});
			return;
		}
	}
  }else{
	var invNumber = '';
	var invMobile = '';
	var invEmail  = '';
  }
  $.get("flow.php",{
	  step:"change_needinv", 
		  need_inv:needInv,
		  inv_type:encodeURIComponent(invType),
		  inv_payee:invPayee,
		  inv_number:invNumber,
		  inv_content:encodeURIComponent(invContent),
		  inv_mobile: invMobile,
		  inv_email: invEmail},
		  function (data){
			$("#ordermoneya").html(data.data);
			if(type==0){
				$("#fpneirong").hide();
				$("#hh").removeClass("r_checked2");
			}
			if(invContent){
				$(".news ").show();
			}
			$(".fapiaos").attr("checked", 'true');
			$("#showfpdw").text(invType == '单位' ? invPayee : '个人');
			$("#hh").trigger("click");
			inv_type   = invType;
			inv_payee  = invPayee;
			inv_mobile = invMobile;
			inv_email  = invEmail;
		},
		  'json');
}





/*
	改变收货地址
*/

function selectshouhuo(obj){
	if (selectedshouhuo == obj)
  {
    return;
  }
  else
  {
    selectedshouhuo = obj;
  }
  $.get("flow.php",{step:"select_shouhuo",address_id:obj.value},orderShippingSelectedResponse,"json");return;
}




/* *
 * 改变配送方式
 */
function selectShipping(obj)
{	
  if (selectedShipping == obj)
  {
    return;
  }
  else
  {
    selectedShipping = obj;
  }
  /*
  var supportCod = obj.attributes['supportCod'].value + 0;
  var theForm = obj.form;

  for (i = 0; i < theForm.elements.length; i ++ )
  {
    if (theForm.elements[i].name == 'payment' && theForm.elements[i].attributes['isCod'].value == '1')
    {
      if (supportCod == 0)
      {
        theForm.elements[i].checked = false;
        theForm.elements[i].disabled = true;
      }
      else
      {
        theForm.elements[i].disabled = false;
      }
    }
  }

  if (obj.attributes['insure'].value + 0 == 0)
  {
    document.getElementById('ECS_NEEDINSURE').checked = false;
    document.getElementById('ECS_NEEDINSURE').disabled = true;
  }
  else
  {
    document.getElementById('ECS_NEEDINSURE').checked = false;
    document.getElementById('ECS_NEEDINSURE').disabled = false;
  }
	*/
  var now = new Date();
  $.get("flow.php",{step:"select_shipping",shipping:obj.value},orderShippingSelectedResponse,"json");return;
  Ajax.call('flow.php?step=select_shipping', 'shipping=' + obj.value, orderShippingSelectedResponse, 'GET', 'JSON');
}

/**
 *
 */
function orderShippingSelectedResponse(result)
{
  if (result.need_insure)
  {
    try
    {
      document.getElementById('ECS_NEEDINSURE').checked = true;
    }
    catch (ex)
    {
      alert(ex.message);
    }
  }

  try
  {
    if (document.getElementById('ECS_CODFEE') != undefined)
    {
      document.getElementById('ECS_CODFEE').innerHTML = result.cod_fee;
    }
  }
  catch (ex)
  {
    alert(ex.message);
  }

  orderSelectedResponse(result);
}

/* *
 * 改变支付方式
 */
function selectPayment(obj)
{	
	/*改过 单选 字体颜色变化*/
	//$(".payment_s").css("color",'#626262');
	//$("#payment"+obj.value).css("color",'red');
	if ($('input[name="add_finsh"]').val() == 0){
		layer.msg('请选保存收货人信息');
		obj.checked = false;
		return;
	}
	if (obj.value == '9'){
		$('#bank_pay_desc').show();
	}else{
		$('#bank_pay_desc').hide();
	}
	if (obj.value == '12' || obj.value == '16' || obj.value == '20'){
		$('#is_hidden_money').hide();
	}else{
		$('#is_hidden_money').show();
	}
	$.get("flow.php",{step:"select_payment",payment:obj.value},orderSelectedResponse,'json');
  //Ajax.call('flow.php?step=select_payment', 'payment=' + obj.value, orderSelectedResponse, 'GET', 'JSON');
}
/* *
 * 团购购物流程 --> 改变配送方式
 */
function handleGroupBuyShipping(obj)
{
	alert("asdfasdfasdf");
  if (groupBuyShipping == obj)
  {
    return;
  }
  else
  {
    groupBuyShipping = obj;
  }

  var supportCod = obj.attributes['supportCod'].value + 0;
  var theForm = obj.form;

  for (i = 0; i < theForm.elements.length; i ++ )
  {
    if (theForm.elements[i].name == 'payment' && theForm.elements[i].attributes['isCod'].value == '1')
    {
      if (supportCod == 0)
      {
        theForm.elements[i].checked = false;
        theForm.elements[i].disabled = true;
      }
      else
      {
        theForm.elements[i].disabled = false;
      }
    }
  }

  if (obj.attributes['insure'].value + 0 == 0)
  {
    document.getElementById('ECS_NEEDINSURE').checked = false;
    document.getElementById('ECS_NEEDINSURE').disabled = true;
  }
  else
  {
    document.getElementById('ECS_NEEDINSURE').checked = false;
    document.getElementById('ECS_NEEDINSURE').disabled = false;
  }

  Ajax.call('group_buy.php?act=select_shipping', 'shipping=' + obj.value, orderSelectedResponse, 'GET');
}

/* *
 * 团购购物流程 --> 改变支付方式
 */
function handleGroupBuyPayment(obj)
{
  if (groupBuyPayment == obj)
  {
    return;
  }
  else
  {
    groupBuyPayment = obj;
  }

  Ajax.call('group_buy.php?act=select_payment', 'payment=' + obj.value, orderSelectedResponse, 'GET');
}

/* *
 * 改变商品包装
 */
function selectPack(obj)
{
  if (selectedPack == obj)
  {
    return;
  }
  else
  {
    selectedPack = obj;
  }

  Ajax.call('flow.php?step=select_pack', 'pack=' + obj.value, orderSelectedResponse, 'GET', 'JSON');
}

/* *
 * 改变祝福贺卡
 */
function selectCard(obj)
{
  if (selectedCard == obj)
  {
    return;
  }
  else
  {
    selectedCard = obj;
  }

  Ajax.call('flow.php?step=select_card', 'card=' + obj.value, orderSelectedResponse, 'GET', 'JSON');
}

/* *
 * 选定了配送保价
 */
function selectInsure(needInsure)
{
  needInsure = needInsure ? 1 : 0;

  Ajax.call('flow.php?step=select_insure', 'insure=' + needInsure, orderSelectedResponse, 'GET', 'JSON');
}

/* *
 * 团购购物流程 --> 选定了配送保价
 */
function handleGroupBuyInsure(needInsure)
{
  needInsure = needInsure ? 1 : 0;

  Ajax.call('group_buy.php?act=select_insure', 'insure=' + needInsure, orderSelectedResponse, 'GET', 'JSON');
}

/* *
 * 回调函数
 */
function orderSelectedResponse(result)
{
  if (result.error)
  {
    alert(result.error);
	//layer.alert(result.error);
   // location.href = './';
  }

  try
  {
    var layer = document.getElementById("ordermoneya");
    layer.innerHTML = (typeof result == "object") ? result.content : result;

    if (result.payment != undefined)
    {
      var surplusObj = document.forms['theForm'].elements['surplus'];
      if (surplusObj != undefined)
      {
        surplusObj.disabled = result.pay_code == 'balance';
      }
    }
  }
  catch (ex) { }
}

/* *
 * 改变余额
 */
function changeSurplus(val)
{
  if (selectedSurplus == val)
  {
    return;
  }
  else
  {
    selectedSurplus = val;
  }

  Ajax.call('flow.php?step=change_surplus', 'surplus=' + val, changeSurplusResponse, 'GET', 'JSON');
}

/* *
 * 改变余额回调函数
 */
function changeSurplusResponse(obj)
{
  if (obj.error)
  {
    try
    {
      document.getElementById("ECS_SURPLUS_NOTICE").innerHTML = obj.error;
      document.getElementById('ECS_SURPLUS').value = '0';
      document.getElementById('ECS_SURPLUS').focus();
    }
    catch (ex) { }
  }
  else
  {
    try
    {
      document.getElementById("ECS_SURPLUS_NOTICE").innerHTML = '';
    }
    catch (ex) { }
    orderSelectedResponse(obj.content);
  }
}

/* *
 * 改变积分
 */
function changeIntegral(val)
{
  val = val ? val : $("input[name=jifen_num]").val();
  if(isNaN(val)){
	layer.msg("请输入正确的积分数字", {time:2000});
	return;
  }
  $.get("flow.php",{step:"change_integral",points:val},changeIntegralResponse,'json');
  Ajax.call('flow.php?step=change_integral', 'points=' + val, changeIntegralResponse, 'GET', 'JSON');
}

/* *
 * 改变积分回调函数
 */
function changeIntegralResponse(obj)
{
  if (obj.error)
  {
    layer.msg(obj.error, {time:2000});
  }
  else
  {
    try
    { layer.msg('使用积分抵现成功', {time:2000});
      document.getElementById('ECS_INTEGRAL_NOTICE').innerHTML = '';
	  $(".jifen_div").hide();
    }
    catch (ex) { }
    orderSelectedResponse(obj.content);
  }
}

/* *
 * 改变红包
 */
function changeBonus(val)
{
  if ($('input[name="add_finsh"]').val() == 0){
	layer.msg('请先保存收货信息');
	return false;
  }
  val = val ? val : $("#sel_bonus").val();
  $.get("flow.php",{step:"change_bonus",bonus:val},changeBonusResponse,'json');return;
  Ajax.call('flow.php?step=change_bonus', 'bonus=' + val, changeBonusResponse, 'GET', 'JSON');
}


/* *
 * 改变红包
 */
function changeBonus_sn()
{
  if ($('input[name="add_finsh"]').val() == 0){
	layer.msg('请先保存收货信息');
	return false;
  }
  val =  $("input[name=bouns_sn]").val();
  $.get("flow.php",{step:"validate_bonus",'bonus_sn':val},changeBonusResponse,'json');return;
  Ajax.call('flow.php?step=change_bonus', 'bonus=' + val, changeBonusResponse, 'GET', 'JSON');
}


/* *
 * 改变红包的回调函数
 */
function changeBonusResponse(obj)
{
  if (obj.error)
  {
	layer.msg(obj.error, {time: 2000});

    try
    {
      document.getElementById('sel_bonus').value = '0';
    }
    catch (ex) { }
  }
  else
  {
	  layer.msg('兑换完成', {time:2000});
  }
  orderSelectedResponse(obj.content);
}

/**
 * 验证红包序列号
 * @param string bonusSn 红包序列号
 */
function validateBonus(bonusSn)
{
  Ajax.call('flow.php?step=validate_bonus', 'bonus_sn=' + bonusSn, validateBonusResponse, 'GET', 'JSON');
}

function validateBonusResponse(obj)
{

if (obj.error)
  {
    alert(obj.error);
    orderSelectedResponse(obj.content);
    try
    {
      document.getElementById('ECS_BONUSN').value = '0';
    }
    catch (ex) { }
  }
  else
  {
    orderSelectedResponse(obj.content);
  }
}

/* *
 * 改变发票的方式
 */
function changeNeedInv()
{
  var obj        = document.getElementById('ECS_NEEDINV');
  var objType    = document.getElementById('ECS_INVTYPE');
  var objPayee   = document.getElementById('ECS_INVPAYEE');
  var objContent = document.getElementById('ECS_INVCONTENT');
  var needInv    = obj.checked ? 1 : 0;
  var invType    = obj.checked ? (objType != undefined ? objType.value : '') : '';
  var invPayee   = obj.checked ? objPayee.value : '';
  var invContent = obj.checked ? objContent.value : '';
  objType.disabled = objPayee.disabled = objContent.disabled = ! obj.checked;
  if(objType != null)
  {
    objType.disabled = ! obj.checked;
  }

  Ajax.call('flow.php?step=change_needinv', 'need_inv=' + needInv + '&inv_type=' + encodeURIComponent(invType) + '&inv_payee=' + encodeURIComponent(invPayee) + '&inv_content=' + encodeURIComponent(invContent), orderSelectedResponse, 'GET');
}

/* *
 * 改变发票的方式
 */
function groupBuyChangeNeedInv()
{
  var obj        = document.getElementById('ECS_NEEDINV');
  var objPayee   = document.getElementById('ECS_INVPAYEE');
  var objContent = document.getElementById('ECS_INVCONTENT');
  var needInv    = obj.checked ? 1 : 0;
  var invPayee   = obj.checked ? objPayee.value : '';
  var invContent = obj.checked ? objContent.value : '';
  objPayee.disabled = objContent.disabled = ! obj.checked;

  Ajax.call('group_buy.php?act=change_needinv', 'need_idv=' + needInv + '&amp;payee=' + invPayee + '&amp;content=' + invContent, null, 'GET');
}

/* *
 * 改变缺货处理时的处理方式
 */
function changeOOS(obj)
{
  if (selectedOOS == obj)
  {
    return;
  }
  else
  {
    selectedOOS = obj;
  }

  Ajax.call('flow.php?step=change_oos', 'oos=' + obj.value, null, 'GET');
}

/* *
 * 检查提交的订单表单
 */
function checkOrderForm(frm)
{
  var paymentSelected = false;
  var shouhuoSelected= false;
  var shippingSelected = false;
  // 检查是否选择了支付配送方式
  for (i = 0; i < frm.elements.length; i ++ )
  {
    if ($('input:radio[name="payment"]:checked').val())
    {
      shippingSelected = true;
    }

    if ($('input:radio[name="userInfoId"]:checked').val())
    {
      paymentSelected = true;
    }
	if ($('input:radio[name="shipping"]:checked').val())
    {
      shouhuoSelected = true;
    }
  }

  /*if ( $("input[name=add_finsh]").val()!=1)
  {
	layer.msg('请选择或填写完善的收货地址');
   // alert('你必须选择一个收货地址');
    return false;
  }

  if (!$('.new_add').is(":hidden")){
	  layer.msg('请保存收货信息');
	  return false;
  }*/

  if (!shouhuoSelected){
	  layer.msg('你必须选择一个配送方式');
	  return false;
  }

  if ($('input[name="add_finsh"]').val() == 0){
	layer.msg('请保存收货信息');
	return false;
  }

  if ( ! shippingSelected)
  {
	layer.msg('你必须选择一个支付方式');
    return false;
  }

	if (!$("input[name=deliverdate]").val())
	{
		layer.msg('请选择送货日期');
		return false;
	}
	var shipping = $('input:radio[name="shipping"]:checked').val();
	if (shipping != '12'){
		if (!$("select[name=delivertime]").val())
		{
			layer.msg('请选择送货时间');
			return false;
		}
		//var one=$('select[name=delivertime]').prop('selectedIndex');;
		//var tow=$('select[name=deliverminute]').prop('selectedIndex');;
		var one = $("select[name='delivertime']").find("option:selected").val();
		var tow = $("select[name='deliverminute']").find("option:selected").val();
		if(tow < one ){
			layer.msg('送货时间段冲突');
			return false;
		}
	}

  // 检查用户输入的余额
  if (document.getElementById("ECS_SURPLUS"))
  {
    var surplus = document.getElementById("ECS_SURPLUS").value;
    var error   = Utils.trim(Ajax.call('flow.php?step=check_surplus', 'surplus=' + surplus, null, 'GET', 'TEXT', false));

    if (error)
    {
      try
      {
        document.getElementById("ECS_SURPLUS_NOTICE").innerHTML = error;
      }
      catch (ex)
      {
      }
      return false;
    }
  }

  // 检查用户输入的积分
  if (document.getElementById("ECS_INTEGRAL"))
  {
    var integral = document.getElementById("ECS_INTEGRAL").value;
    var error    = Utils.trim(Ajax.call('flow.php?step=check_integral', 'integral=' + integral, null, 'GET', 'TEXT', false));

    if (error)
    {
      return false;
      try
      {
        document.getElementById("ECS_INTEGRAL_NOTICE").innerHTML = error;
      }
      catch (ex)
      {
      }
    }
  }
  $('.submit_done').attr('disabled', true);
  layer.msg('订单已提交，请稍等...', {time:100000});
  frm.action = frm.action + '?step=done';
  return true;
}

/* *
 * 检查收货地址信息表单中填写的内容
 */
function checkConsignee(frm)
{
  var msg = new Array();
  var err = false;

  if (frm.elements['country'] && frm.elements['country'].value == 0)
  {
    msg.push(country_not_null);
    err = true;
  }

  if (frm.elements['province'] && frm.elements['province'].value == 0 && frm.elements['province'].length > 1)
  {
    err = true;
    msg.push(province_not_null);
  }

  if (frm.elements['city'] && frm.elements['city'].value == 0 && frm.elements['city'].length > 1)
  {
    err = true;
    msg.push(city_not_null);
  }

  if (frm.elements['district'] && frm.elements['district'].length > 1)
  {
    if (frm.elements['district'].value == 0)
    {
      err = true;
      msg.push(district_not_null);
    }
  }

  if (Utils.isEmpty(frm.elements['consignee'].value))
  {
    err = true;
    msg.push(consignee_not_null);
  }

  if ( ! Utils.isEmail(frm.elements['email'].value))
  {
    err = true;
    msg.push(invalid_email);
  }

  if (frm.elements['address'] && Utils.isEmpty(frm.elements['address'].value))
  {
    err = true;
    msg.push(address_not_null);
  }

  if (frm.elements['zipcode'] && frm.elements['zipcode'].value.length > 0 && (!Utils.isNumber(frm.elements['zipcode'].value)))
  {
    err = true;
    msg.push(zip_not_num);
  }

  if (Utils.isEmpty(frm.elements['tel'].value))
  {
    err = true;
    msg.push(tele_not_null);
  }
  else
  {
    if (!Utils.isTel(frm.elements['tel'].value))
    {
      err = true;
      msg.push(tele_invaild);
    }
  }

  if (frm.elements['mobile'] && frm.elements['mobile'].value.length > 0 && (!Utils.isTel(frm.elements['mobile'].value)))
  {
    err = true;
    msg.push(mobile_invaild);
  }

  if (err)
  {
    message = msg.join("\n");
    alert(message);
  }
  return ! err;
}



/*
	兼容模式加入购物车
*/
function addToCart_compatible(goodsId, parentId,type)
{
  var goods        = new Object();
  var spec_arr     = new Array();
  var str_spec     = '';
  var fittings_arr = new Array();
  var number       = 1;
  var formBuy      = document.forms['ECS_FORMBUY'];
  var quick		   = 0;
 /*
  // 检查是否有商品规格 
  if (formBuy)
  {
    spec_arr = getSelectedAttributes(formBuy);

    if (formBuy.elements['number'])
    {
      number = formBuy.elements['number'].value;
    }
	quick = 1;
  }
  */
 
  quick = 1;	

  

  var obj      = document .getElementById("number");

  if(obj){
	number=obj.value;
  }
  var attr= document.getElementsByName("spec_list[]");
  for (i = 0; i < attr.length; i ++ )
  {
     str_spec+= str_spec ?  ","+attr[i].value: attr[i].value;
	
  }
  str_spec  =str_spec ? str_spec : '';


  goods.quick    = quick;
  goods.type	 = type;
  goods.spec     = str_spec;
  goods.goods_id = goodsId;
  goods.number   = number;
  goods.parent   = (typeof(parentId) == "undefined") ? 0 : parseInt(parentId);
	
  ajaxs({
	type:"post",
	url:"flow.php?step=add_to_cart&goods="+JSON.stringify(goods),
	data:"123",
	dataType:"json",
	success:function(data){
		if(data.error==0){
			location.reload();
		}else{
			 //layer.msg(data.message, {shift: 6});
			 //layer.msg(data.message, {shift: 1,icon: 2});
			 alert(data.message);
			 return;
		}
	}
 });
  return;
  $.post("flow.php",{step:"add_to_cart",goods:JSON.stringify(goods)},addToCartResponse,"json");
 }


//修改收货人信息
function updateConsignee(check, shipping){
	//var shipping     = typeof shipping == 'undefined' ? $('input:radio[name="shipping"]:checked').val() : shipping;
	$.post('yolin.php?t='+Math.random(), {step:'consignee_ajax_update', check:check, shipping:shipping}, function(result){
		$('#address').html((typeof result == "object") ? result.content : result);
	}, 'json');
}