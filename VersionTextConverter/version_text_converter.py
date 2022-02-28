import glob
import os
import re
import json
import time
import define

__version__ = "1.1.0"

# バージョン情報のテキストを数字に変換する
def version_text_to_num(version):
	try:
		reg = r'([0-9]*?)\.([0-9]*?)\.([0-9]*?)$'
		result = re.match(reg, version)
		return [int(result.group(1)), int(result.group(2)), int(result.group(3))]
	except Exception:
		return [0, 0, 0]
	return

# HTML記号をエスケープする
def escape_html(text):
	for row in define.HTML_ESCAPE_TABLE:
		text = text.replace(row[0], row[1])
	return text


file_path_list = glob.glob("./*.txt")
update_info_list = []

for file_path in file_path_list:
	with open(file_path, "r", encoding=define.CHARACTER_ENCODING) as f:
		text = f.read()
		tbody = ""
		combining_flag = False			# セル結合フラグ

		reg_info = r'[\s\S]*?ver\.([\s\S]*?)\s\(([0-9/]{8,10})\)([\s\S]*?)\n([\s\S]*?)-{5,300}[\s\S]*?'
		for row in re.finditer(reg_info, text, re.MULTILINE):
			reg_title = r'.*?\[(.*?)\].*?'
			reg_title_result = re.match(reg_title, row.group(3))
			if reg_title_result:
				update_title = reg_title_result.group(1)
			else:
				update_title = ""
			#print(row.group(1))
			#print(row.group(2))
			#print(update_title)
			#print(row.group(4).rstrip("\n"))
			#print("#"*60)
			update_info_list.append({
				define.JSON_KEY.date: row.group(2),
				define.JSON_KEY.file_name: os.path.splitext(os.path.basename(file_path))[0],
				define.JSON_KEY.version: row.group(1),
				define.JSON_KEY.title: update_title
			})

			indent_num = 3
			tbody += "\t"*indent_num + "<tr>\n"
			version_num_list = version_text_to_num(row.group(1))
			if version_num_list[2] == 0:			# 新要素追加のアップデートなら
				if not combining_flag:				# 結合されたセルでなければ通常通り処理する
					tbody += "\t"*(indent_num + 1) + '<td class="center">{}</td>\n'.format(update_title)
				else:								# 結合されたセルの一番最初のバージョンなら更新タイトルを参照する
					tbody = tbody.format(title=update_title)
					combining_flag = False
			else:									# バグ修正のアップデートなら
				if not combining_flag:				# 一番上のバージョンにタイトルセルを結合する
					tbody += "\t"*(indent_num + 1) + '<td class="center" rowspan="{}">{}</td>\n'.format(version_num_list[2] + 1, "{title}")
					combining_flag = True
			tbody += "\t"*(indent_num + 1) + '<td class="center">{}</td>\n'.format(row.group(1))			# バージョン
			datetime_str = re.sub(r'^(.*?)/(.*?)/(.*?)$', r'\1年\2月\3日', row.group(2))
			tbody += "\t"*(indent_num + 1) + '<td class="center">{}</td>\n'.format(datetime_str)			# 日付
			contents = row.group(4).rstrip("\n")							# 更新内容
			contents = escape_html(contents)
			contents_list = contents.split("\n\n", 1)						# 機能追加と不具合修正で分割する
			for i in range(len(contents_list)):
				contents_list[i] = contents_list[i].replace("\n", "<br>\n" + "\t"*(indent_num + 4))
			contents = define.BOX_HTML.format(title="機能追加", color="royalblue", back_color="aliceblue", text=contents_list[0])
			if version_num_list[2] != 0:			# 不具合修正だけのバージョンなら最初の塊から不具合修正にする
				contents = define.BOX_HTML.format(title="不具合修正と調整", color="orange", back_color="lightgoldenrodyellow", text=contents_list[0])
			if len(contents_list) == 2:
				contents += define.BOX_HTML.format(title="不具合修正と調整", color="orange", back_color="lightgoldenrodyellow", text=contents_list[1])
			tbody += "\t"*(indent_num + 1) + "<td>{}\n".format(contents) + "\t"*(indent_num + 1) + "</td>\n"
			tbody += "\t"*indent_num + "</tr>\n"

		
		table = define.TABLE_HTML.format(tbody=tbody)
		html_text = define.HTML_TEMPLATE.format(title="更新履歴", description="ツールの更新履歴", body=table, version=__version__)
		out_file_path = os.path.splitext(file_path)[0] + ".html"
		with open(out_file_path, "w", encoding=define.CHARACTER_ENCODING) as f:
			f.write(html_text)
		print("\n\n更新履歴をHTMLへ変換しました\n{}\n".format(out_file_path))

export_json = True
if export_json:
	json_str = json.dumps(update_info_list, indent=4, ensure_ascii=False)		# 文字列として出力する
	with open(define.EXPORT_JSON_PATH, "w", encoding="utf-8") as f:
		f.write(json_str)												# ファイルに出力する
		print(f"読み込んだ全ての更新情報をjsonに出力しました\n{define.EXPORT_JSON_PATH}\n")

time.sleep(10)

'''     更新履歴
----------------------------------------------------------------------------------------------------------
ver.1.1.0 (2022/01/30)
htmlに変換した全てのファイルの更新情報をまとめてjsonに出力する機能を追加

----------------------------------------------------------------------------------------------------------
ver.1.0.1 (2021/10/16)
生成されるHTMLの最後にバージョン情報を含むコメントを追加
<p>タグ内の文章の一行目が改行されていない不具合を修正
<table>タグが<body>タグと同じインデントになっていた不具合を修正
</tbody>タグが正常にインデントされていない不具合を修正

----------------------------------------------------------------------------------------------------------
ver.1.0.0 (2021/09/26)
リリース
'''