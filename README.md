# system_design

exeディレクトリの中に色々入ってます
ごちゃごちゃしてて使いづらいですが悪しからず。
時間があればまとめときます。

#sdfファイルをUFFで３次元配座に変換 : rdk.py
	
	./mol_datas 内のsdfファイルを３次元配座に変換します。

#sdfファイル → pdbファイル →pdbqtファイルまで変換 : sdf_to_pdbqt.sh

	./mol_datas 内のsdfファイルをpdbqtファイルに変換します。

	"*.sh"の実行は、コマンドラインで"chmod 755 *.sh"で実行権限を与えてから
                               "sh *.sh"で実行できます。

#各pdbqtファイルに対応したvina用のinputファイルの作成 : make_vina_txt.py
	
	./mol_datas 内のpdbqtファイルに対応したtxtファイルを ./txt_datasに格納します。
	(標的タンパク質に応じて変更)

# ./txtdatas内のtxtファイルに対してvinaによるドッキングシミュレーションを行う : vina_exe.sh

	./txt_datas 内の全txtに対してループ回してます。
	logファイルは ./log_datas に格納します。

#logファイルの集計 : sum_log.py
	logファイルを集計して、CAS_numberとaffinityを "sum_log.csv"へ格納
	同時にaffinityだけを"y_all.py"へ格納
	今回は1154構造

#sum_log.csvのCASに対応する構造記述子データをとってくる : extract_x.py

	(今回は1154構造の)CASに対応したデータを"x_all.csv"へ格納

#PEIOPT.py用の学習用データ及びテスト用データの用意 : make_model_data.py {学習用データとして取り出したい数}
	
	x_all.csv および y_all.csvから指定した個数の学習用データをランダムに抽出 "x.csv","y.csv"へ
	残りをテスト用データとして、"xeval.csv","yeval.csv"へ



