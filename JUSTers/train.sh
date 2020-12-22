python run_lm_finetuning.py \
--train_data_file data_dir/training \
--output_dir $1 \
--model_type gpt2-medium \
--eval_data_file data_dir/development \
--model_name_or_path gpt2-medium \
--block_size 128 \
--do_train \
--do_eval \
--per_gpu_train_batch_size $2 \
--per_gpu_eval_batch_size $2 \
--gradient_accumulation_steps $3 \
--num_train_epochs $4 \
--save_steps 9000000000 \
--eval_all_checkpoints \
--overwrite_output_dir \
--overwrite_cache \
--logging_steps 1
