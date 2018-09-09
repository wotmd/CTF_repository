<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, maximum-scale=0.75">
	<meta http-equiv="X-UA-Compatible" content="IE=edge;chrome=1" />
	<link rel="apple-touch-icon" sizes="57x57" href="icon/apple-icon-57x57.png">
	<link rel="apple-touch-icon" sizes="60x60" href="icon/apple-icon-60x60.png">
	<link rel="apple-touch-icon" sizes="72x72" href="icon/apple-icon-72x72.png">
	<link rel="apple-touch-icon" sizes="76x76" href="icon/apple-icon-76x76.png">
	<link rel="apple-touch-icon" sizes="114x114" href="icon/apple-icon-114x114.png">
	<link rel="apple-touch-icon" sizes="120x120" href="icon/apple-icon-120x120.png">
	<link rel="apple-touch-icon" sizes="144x144" href="icon/apple-icon-144x144.png">
	<link rel="apple-touch-icon" sizes="152x152" href="icon/apple-icon-152x152.png">
	<link rel="apple-touch-icon" sizes="180x180" href="icon/apple-icon-180x180.png">
	<link rel="icon" type="image/png" sizes="192x192"  href="icon/android-icon-192x192.png">
	<link rel="icon" type="image/png" sizes="32x32" href="icon/favicon-32x32.png">
	<link rel="icon" type="image/png" sizes="96x96" href="icon/favicon-96x96.png">
	<link rel="icon" type="image/png" sizes="16x16" href="icon/favicon-16x16.png">
	<link rel="manifest" href="icon/manifest.json">
	<meta name="msapplication-TileColor" content="#ffffff">
	<meta name="msapplication-TileImage" content="icon/ms-icon-144x144.png">
	<meta name="theme-color" content="#ffffff">
	<meta name="apple-mobile-web-app-capable" content="yes">
	<meta name="mobile-web-app-capable" content="yes">
	<title>ARKANOID</title>
	<link rel="stylesheet" type="text/css" href="style/style_v.css" />
	<script type="text/javascript" src="script_loader.php?fn=jsbn.js"></script>
	<script type="text/javascript" src="script_loader.php?fn=rsa.js"></script>
	<script type="text/javascript" src="script_loader.php?fn=prng4.js"></script>
	<script type="text/javascript" src="script_loader.php?fn=rng.js"></script>
</head>

<body>
	<div id="arkanoid" style="visibility: hidden;">
		<div id="mobile_title_back" width="450">
			<h1 id="mobile_title" style="margin-top: 0.2em; margin-bottom: 0.2em;"><span style="color: rgb(98, 132, 209);">A</span>RKANOID</h1>
			<ul class="mobile_menu"> 
				<li class="mobile_menu_item menu_selected">게임 화면</li>
				<li class="mobile_menu_item">설정/기록</li>
			</ul>
		</div>
		<div id="canvas_back" width="450" height="580">
			<canvas id="canvas" width="450" height="580"></canvas>
		</div>
		<div id="info_back" width="350" height="580">
			<h1 id="info_name"><span style="color: rgb(98, 132, 209);">A</span>RKANOID</h1>
			<p id="instruction_label" class="label">조작법</p>
			<div id="instruction">←,→키 또는 마우스로 조정</div>
			<p id="volume_label" class="label">볼륨 설정<span style="font-weight: normal; font-size: 0.65em; margin-left: 0.5em;">(배경음은 게임 시작시 나옴)</span>
			</p>
			<div id="volume_main">
				<input type="range" id="volume" value="100">
				<button type="button" id="muted" class="blue_btn">◈</button>
				<button type="button" id="muted_se" class="blue_btn">◈</button>
			</div>
			<p id="scoreboard_label" class="label">기록<span id="scoreboard_reset">(삭제)</span>
			</p>
			<div id="scoreboard_main">
				<table id="scoreboard">
					<thead>
						<tr><th>#</th><th>Score</th><th>Date</th></tr>
					</thead>
					<tbody>
						<tr><td>1</td><td></td><td></td></tr>
						<tr><td>2</td><td></td><td></td></tr>
						<tr><td>3</td><td></td><td></td></tr>
						<tr><td>4</td><td></td><td></td></tr>
						<tr><td>5</td><td></td><td></td></tr>
						<tr><td>6</td><td></td><td></td></tr>
						<tr><td>7</td><td></td><td></td></tr>
						<tr><td>8</td><td></td><td></td></tr>
						<tr><td>9</td><td></td><td></td></tr>
						<tr><td>10</td><td></td><td></td></tr>
					</tbody>
				</table>
			</div>
		</div>
	</div>
	<footer id="footer">
		<p>Copyright ⓒ 2014-2015 Alias Nashira.</p>
		<address id="footmail">
			Email: <a id="mailaddress" href="mailto:alias_n@live.com">alias_n@live.com</a>
		</address>
		<p id="imgsrc"><a href="source.php">See Media Source</a></p>
	</footer>
	<script type="text/javascript" src="script_loader.php?fn=script.js"></script>
	<!-- You can see the challenge when you first clear the game once. -->		</body>

</html>