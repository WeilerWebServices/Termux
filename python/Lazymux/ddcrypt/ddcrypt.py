# ddcrypt v1.0 - by Gameye98/DedSecTL
# droidscript deobfuscator - note that when droidscript update, their app function code will always change
# so dont blame me if you found the function code its not match with real function code, i dont think you understand what ive said
# i dont even know what im saying, just do the experiment by yourself and you will understand what im trynna say
# ---
# license: MIT
# team: BlackHole Security
# purpose: droidscript apk deobfuscator
# ---
import os, re, sys, time

if len(sys.argv) != 2:
	print(f"Usage: {sys.argv[0]} filename.js")
else:
	filepath = sys.argv[1]
	if os.path.exists(sys.argv[1]):
		if os.path.isfile(filepath):
			print("[ddcrypt] starting...")
			code_fix = [["),",")\n"],["(!1)","(false)"],["(1)","(true)"],[")\n",");\n\t"],["(){","() {\n\t"],[",.",",0."],["!1)","false)"],[")}function",");\n}\nfunction"],[" =  = "," == "],["case\"","case \""],["1?","true"],[")):",");} else {"],["try{","try {\n\t"],[";while",";\n\twhile"],["++}","++;\n}"],[";break;case",";break;\n\tcase"],[":app",": app"],["}function","}\nfunction"],["}catch(e){","} catch(e) {\n\t"],[")}}",");\n\t}\n}"],["\"?","\") {\n\t"],[")}",")\n}"]]
			funclst = ["_103:ShowPopup","_2():Exit()","_130:SetOrientation","_86:EnableBackKey","_126:SetOrientation","_84:EnableBackKey","_88:Alert","_264:CreateListDialog","_239:CreateButton","_244:CreateText","_245:CreateTextEdit","_248:CreateScroller","_257:CreateScroller","_158:AddLayout","_182:ReadFile","_237:CreateLayout","_254:CreateYesNoDialog"]
			filename = filepath.split("/")[len(filepath.split("/"))-1]
			print(f"[read] file: {filepath}")
			filenew = filename.replace(".js","")+"_new.js"
			fileold = filename.replace(".js","")+"_old.js"
			bak = inx = open(sys.argv[1], "r").read()
			reg_1 = re.findall(r'\\u\d\d\d\d', inx)
			reg_2 = re.findall(r'\\u\d\d\d\w', inx)
			reg_3 = re.findall(r'\w+=\w+', inx)
			# reg_4 = re.findall(r'\w+,\w+', inx)
			reg_5 = re.findall(r'"=\w+', inx)
			reg_6 = re.findall(r'\w+="', inx)
			print(f"[{filename}] deobfuscating code (regex+unicode)")
			for item in reg_1:
				exec(f"res = u'{item}'")
				inx = inx.replace(item, res)
			for item in reg_2:
				exec(f"res = u'{item}'")
				inx = inx.replace(item, res)
			for item in reg_3:
				inx = inx.replace(item, item.replace("="," = "))
			"""
			for item in reg_4:
				inx = inx.replace(item, item.replace(",",";\n"))
			"""
			for item in reg_5:
				inx = inx.replace(item, item.replace("="," = "))
			for item in reg_6:
				inx = inx.replace(item, item.replace("="," = "))
			dd_0 = inx
			print(f"[{filename}] fix code depends on code_fix[]")
			for piece_of in code_fix:
				dd_0 = dd_0.replace(piece_of[0], piece_of[1])
			"""
			dd_1 = dd_0.replace("),",")\n")
			dd_2 = dd_1.replace("(!1)","(false)").replace("(1)","(true)")
			dd_3 = dd_2.replace(")\n",");\n\t")
			dd_4 = dd_3.replace("="," = ")
			dd_5 = dd_4.replace("(){","() {\n\t")
			dd_6 = dd_5.replace(",.",",0.").replace("!1)","false)")
			dd_7 = dd_6.replace(")}function",");\n}\nfunction")
			dd_8 = dd_7.replace(" =  = "," == ")
			dd_9 = dd_8.replace("case\"","case \"")
			dd_10 = dd_9.replace("1?","true")
			dd_11 = dd_10.replace(")):",");} else {")
			dd_12 = dd_11.replace("try{","try {\n\t")
			"""
			print(f"[{filename}] replace old function with new function")
			for function in funclst:
				dd_0 = dd_0.replace(function.split(":")[0],function.split(":")[1])
				time.sleep(0.1)
			open(filepath,"w").write(dd_0)
			print(f"[write] original: {filepath}")
			open(filenew,"w").write(dd_0)
			print(f"[write] backup(new): {filenew}")
			open(fileold,"w").write(bak)
			print(f"[write] backup(old): {fileold}")
			print("[ddcrypt] done .. !!")