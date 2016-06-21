*必要なファイル
	*2_5_total_strs.zip
	*2_5_total_strs_descriptors.zip
	*PEIopt内
		*gp_test.py
		*history.py
		*history_internal.py
		*temp.py
		*template.py
		*bound.csv
		*option.csv
		*yinf.csv
	*clean_descriptors.py
	*cycle.py
	*extract_y.py
	*make_vina_config.py
	*pdb2pdbqt.py
	*PEIOPT_edit.py
	*rdk.py
	*sampling.py
	*sdf2pdb.py
	*split.py
	
*操作手順
	*unzip 2_5_total_strs.zip
	*unzip 2_5_total_strs_descriptors.zip
	*python3 clean_descriptors.py ※記述子データを整形してX_all.csvに保存
	*mv 2_5_total_strs.sdf 2_5_total_strs.sdf.rename ※*.sdfでの一括処理をしやすくするため
	*python3 split.py 2_5_total_strs.sdf.rename ※1分子ごとに個別のsdfファイルに分ける
	*rm 106770.sdf ※実際には106770にあたる分子はないが、区切りの関係で出てきてしまう。削除
	*コマンドプロンプト上 ※要Anaconda & rdkit.  Anacondaインストール後 conda create -c https://conda.anaconda.org/rdkit -n my-rdkit-env rdkit
		*activate my-rdkit-env
		*WDへ移動
		*python rdk.py ※UFFによりsdfの立体構造最適化
	*python3 sdf2pdb.py ※sdfからpdbに変換
	*python3 pdb2pdbqt.py ※pdbからpdbqtに変換
	*python3 make_vina_configs.py ※vina configファイル作成
	*mkdir sdfs ; mv *.sdf sdfs/
	*mkdir pdbs ; mv *.pdb pdbs/
	*mkdir pdbqts ; mv *.pdbqt pdbqts/
	*mkdir vina_configs ; mv *.config vina_configs/
	*mkdir samples
	*python3 sampling.py ※指定した数の構造を初期入力用にサンプリング
	*cp 3rze_noLigands.pdbqt samples/
	*cp extract_y.py samples/
	*cd samples/
	*find -name "*.config" | xargs -L 1 ./vina.exe --config
	*python3 extract_y.py
	*cp affinity.csv ../y.csv
	*cp structure_ids.csv ../
	*mkdir ../cycle
	*cp 3rze_noLigands.pdbqt ../cycle/
	*cp vina*.exe ../cycle/
	*cd ../
	*cp samples/affinity.csv ./y.csv ※初期のyを用意
	*python3 init_x.py ※初期のX.csv, XEval.csvを用意
	*コマンドプロンプト上
		*python cycle.py


