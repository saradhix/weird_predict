
<!DOCTYPE html>
<html id="ng-app" ng-app="dnsApp" lang="en-US">
<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en-US"> <![endif]-->
<!--[if IE 7]>    <html class="no-js lt-ie9 lt-ie8" lang="en-US"> <![endif]-->
<!--[if IE 8]>    <html class="no-js lt-ie9" lang="en-US"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en-US"> <!--<![endif]-->
<head>
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<meta charset="utf-8" />
<title>Bizarre News Identification </title>
<meta name="description" content="" />
<meta name="keywords" content="" />
<link href="https://img1.wsimg.com/fos/201401/global/css/3.6.0/combined-3.6.0.min.css" rel="stylesheet" type="text/css">
<link href="https://img1.wsimg.com/fos/sales/themes/scotty/domains/search/css/styles10212014.min.css?v=14" rel="stylesheet" type="text/css">
<script src="https://img1.wsimg.com/fos/201401/global/vendor/jquery/1.8.3/jquery.min.js"></script>
<link href="https://img1.wsimg.com/pc_css/1/gd_cds_2014v1_css_20141029.min.css" rel="stylesheet" />
<style type="text/css">
.btn-new-width{min-width: 104px;}
.londonimg {background-image: url("https://img1.wsimg.com/fos/201401/domains/search/img/london.png");}
.left {float:left}
.right {float:right}
.ng-cloak{display: none !important;}
</style>
<!-- Google Tag Manager -->
</head>
<body ng-controller="dnsCtrl" ng-cloak>
<div class="border-box" role="main" style="width:auto">
<!-- Start main-panel -->
<section class="white-bg main-panel">
<h2 class="main-panel-title">Bizarre News Identification</h2>
<form method="GET" action="index.php" class="search-form" id="domain_search_form" style="margin: 0 auto 20px;">
<div class="searchBoxForm">
<input type="text" name="title" value="<?php echo @$_REQUEST['title'];?>" class="search-form-input" placeholder="Enter any news title" autocomplete="off"  style="width:900px; border:none;outline:0;min-width: 500px;" />
<button type="submit" class="btn btn-primary btn-search-form submitbtn">Analyze</button>
<div class="clearfix"></div>

<?php
$title = @$_REQUEST['title'];
if(isset($title))
{


$id=md5(rand(1,10000));
$json_obj=['id'=>$id,'title'=>$title];
#print_r($json_obj);
$json_request = json_encode($json_obj,true);

require("phpMQTT.php");

$mqtt = new phpMQTT("localhost", 1883, $id);
//Change client name to something unique

if ($mqtt->connect()) {
  $mqtt->publish("request",$json_request,0);
  echo "<!--published-->";
}
$topics[$id] = ["qos"=>0, "function"=>"myresponse"];
$mqtt->subscribe($topics,0);
while($mqtt->proc())
{
}

}//End of if isset title
function myresponse($topic, $message)
{
#global $mqtt;
#echo "Entered myresponse with $topic, $message";
$bizarre=rand(1,70);
$normal = 100-$bizarre;

$json_obj = json_decode($message,true);
$bizarre=(int)$json_obj['bizarre'];
$normal = 100-$bizarre;
$title=$json_obj['title'];
include "result_include.php";
#$mqtt->close();
exit();
}

?>
</div>
</form>
</body>
</html>
