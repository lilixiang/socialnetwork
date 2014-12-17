exports.getAvatar = function(uid, path){
  var swfObj = '<object name="c_avatar" type="application/x-shockwave-flash" width="720" height="420" id="c_avatar_miniblog1" align="middle" data="'+ path +'c_avatar.swf">'+
	'<param name="allowScriptAccess" value="always" />' +
	'<param name="allowfullscreen" value="true" />' +
	'<param name="AllowNetworking" value="all" />' +
	'<param name="quality" value="high" />' +
	'<param name="bgcolor" value="#ffffff" />' +
	'<param name="menu" value="false" />' +
	'<param name="flashvars" value="policy_file_url='+ path +'crossdomain.xml&big_avatar_url='+ path +'user/'+ uid +'_big.jpg&middle_avatar_url='+ path +'user/'+ uid +'_middle.jpg&little_avatar_url='+ path +'user/'+ uid +'_small.jpg&big_avatar_name='+ uid +'_big&middle_avatar_name='+ uid +'_middle&little_avatar_name='+ uid +'_small&url_params=" />'+
	'</object>';
  return swfObj;

    $swfObj = '';
};
