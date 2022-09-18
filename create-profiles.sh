MAXPROCS=40

profiling_recipe_dir="/home/ubuntu/ebs_tmp/jump-scope/profiling-recipe_copy/profiles"
config_file_dir="/home/ubuntu/ebs_tmp/jump-scope/config_files"

mkdir "$profiling_recipe_dir/log"

ls $config_file_dir | parallel --max-procs ${MAXPROCS} \
--ungroup \
--eta \
--joblog "$profiling_recipe_dir/log/collate.log" \
--results log/making-profiles \
--files \
--keep-order \
python "$profiling_recipe_dir/profiling_pipeline.py"  --config "$config_file_dir/"{1}