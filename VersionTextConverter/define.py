import enum

class JSON_KEY(str, enum.Enum):
	date = "date"
	file_name = "file_name"
	version = "version"
	title = "title"

CHARACTER_ENCODING = "utf-8"
EXPORT_JSON_PATH = "./update_data.json"
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="ja">
<head>
	<meta charset="utf-8">
	<title>{title}</title>
	<meta name="description" content="{description}">
	<style type="text/css">
		th {{
			background: gainsboro;
		}}

		td.center {{
			text-align: center;
		}}

		.text_box {{
			position: relative;
			margin: 0.5em 0.5em;
			padding: 25px 10px 7px;
			border: solid 2px #FFC107;
		}}

		.text_box .box-title {{
			position: absolute;
			display: inline-block;
			top: -2px;
			left: -2px;
			padding: 0 9px;
			height: 25px;
			line-height: 25px;
			font-size: 17px;
			background: #FFC107;
			color: #ffffff;
			font-weight: bold;
		}}

		.text_box p {{
			margin: 0;
			padding: 0;
		}}
	</style>
</head>

<body>
{body}</body>
<!-- Converted by VersionTextConverter ver.{version} -->
</html>'''

TABLE_HTML = '''	<table border="1" style="border-collapse: collapse;">
		<thead>
			<tr>
				<th>アップデート</th>
				<th>バージョン</th>
				<th>リリース日</th>
				<th>変更内容</th>
			</tr>
		</thead>
		<tbody>
{tbody}\t\t</tbody>
	</table>
'''

BOX_HTML = '''
					<div class="text_box" style="border-color: {color}; background: {back_color};">
						<span class="box-title", style="background: {color};">{title}</span>
						<p>
							{text}
						</p>
					</div>'''

HTML_ESCAPE_TABLE = [
	["&", "&amp;"],
	['"', "&quot;"],
	["'", "&apos;"],
	[">", "&gt;"],
	["<", "&lt;"],
]
