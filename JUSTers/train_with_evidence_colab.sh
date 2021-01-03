python finetune_evidence.py \
--train_data_file ./../Data/justers/training/training \
--output_dir colab_trained \
--model_type gpt2 \
--eval_data_file ./../Data/justers/evaluation/evaluation \
--model_name_or_path gpt2-medium \
--block_size 128 \
--do_train \
--do_eval \
--per_gpu_train_batch_size $1 \
--per_gpu_eval_batch_size $1 \
--gradient_accumulation_steps 5 \
--num_train_epochs 5 \
--save_steps 9000000000 \
--eval_all_checkpoints \
--overwrite_output_dir \
--overwrite_cache \
--learning_rate 1e-4