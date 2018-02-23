
<!DOCTYPE html>
<html id="ng-app" ng-app="dnsApp" lang="en-US">
<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en-US"> <![endif]-->
<!--[if IE 7]>    <html class="no-js lt-ie9 lt-ie8" lang="en-US"> <![endif]-->
<!--[if IE 8]>    <html class="no-js lt-ie9" lang="en-US"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en-US"> <!--<![endif]-->
<head>
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<meta charset="utf-8" />
<title>Timeline Search </title>
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
<div class="border-box" role="main">
<!-- Start main-panel -->
<section class="white-bg main-panel">
<h2 class="main-panel-title">Bizarre News Identification</h2>
<form method="GET" action="index.php" class="search-form" id="domain_search_form" style="margin: 0 auto 20px;">
<div class="searchBoxForm">
<input type="text" name="title" placeholder="Enter any news title" class="search-form-input" id="domain_search_input" autocomplete="off"  style="width:auto; border:none;outline:0;min-width: 500px;" />
<button type="submit" class="btn btn-primary btn-search-form submitbtn">Find</button>
<div class="clearfix"></div>

<?php
$title = @$_REQUEST['title'];
if(isset($title))
{
$bizarre=rand(1,70);
$normal = 100-$bizarre;
?>
<div id="pieChart"></div>
<script src="d3.min.js"></script>
<script src="d3pie.js"></script>
<script>
var pie = new d3pie("pieChart", {
	"header": {
		"title": {
			"text": "<?php echo $title;?>",
			"fontSize": 22,
			"font": "verdana"
		}
	},
	"footer": {
		"color": "#999999",
		"fontSize": 11,
		"font": "open sans",
		"location": "bottom-center"
	},
	"size": {
		"canvasHeight": 400,
		"canvasWidth": 590,
		"pieOuterRadius": "88%"
	},
	"data": {
		"content": [
			{
				"label": "Bizarre",
				"value": <?php echo $bizarre;?>,
				"color": "#697e38"
			},
			{
				"label": "Normal",
				"value": <?php echo $normal;?>,
				"color": "#7e3838"
			}
		]
	},
	"labels": {
		"outer": {
			"pieDistance": 32
		},
		"inner": {
			"format": "value"
		},
		"mainLabel": {
			"font": "verdana"
		},
		"percentage": {
			"color": "#e1e1e1",
			"font": "verdana",
			"decimalPlaces": 0
		},
		"value": {
			"color": "#e1e1e1",
			"font": "verdana"
		},
		"lines": {
			"enabled": true,
			"color": "#cccccc"
		},
		"truncation": {
			"enabled": true
		}
	},
	"effects": {
		"load": {
			"speed": 2000
		},
		"pullOutSegmentOnClick": {
			"effect": "linear",
			"speed": 400,
			"size": 8
		}
	}
});
</script>
<?php





}//End of if isset title
?>
</div>
</form>
</body>
</html>
