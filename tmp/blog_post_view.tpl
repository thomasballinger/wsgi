<!--default template-->
<!--what variables are expected within the default_view view?
a header, and content-->

<DOCTYPE lang="html">
<html>
<head>
	<!--link href="css/style.css" type="text/css" rel="stylesheet"--><!--at the moment, the server doesn't know what to do with a css file-->
	<style>
		body { font-family: sans-serif; background: #eee; }
		a, h1, h2 { color: #377BA8; }
		h1, h2 { font-family: 'Georgia', serif; margin: 0; }
		h1 { border-bottom: 2px solid #eee; }
		h2 { font-size: 1.2em; }
	</style>
</head>
<body>
<h1>'+header+'</h1>
<p>'+content+'</p>
</body>
</html>
