NAME := push_swap
BONUS_NAME := checker

CC := cc
CFLAGS := -Wall -Wextra -Werror
MAKEFLAGS += -j
LIBFT_DIR := Libft
PRINTF_DIR := ft_printf
LIBFT := $(LIBFT_DIR)/libft.a
PRINTF := $(PRINTF_DIR)/libftprintf.a

SRCS := \
	push_swap.c \
	1_main.c \
	2_parse_main.c \
	2-1_parse_number.c \
	2-2_parse_stack.c \
	3_strategy.c \
	4_sort_main.c \
	4-1_simple_sort.c \
	4-2_medium_sort.c \
	4-3_radix_sort.c \
	5_sort_opticsri_main.c \
	5-1_sort_opticsri_calc.c \
	5-2_sort_opticsri_exec.c \
	6_benchmark.c \
	utils-1_is_option.c \
	utils-2_strings_are_equal.c \
	utils-3_is_space.c \
	utils-4_print_error_and_free.c \
	utils-5_free_and_exit_success.c \
	utils-6_free.c \
	utils-7_rank_sort.c \
	utils-7-1_rank_assign.c \
	utils-8_print_operation.c \
	utils-9_swap_stack.c \
	utils-10_push_stack.c \
	utils-11_rotate_stack.c \
	utils-12_reverse_rotate_stack.c \
	utils-13_find_maximum_position.c \
	utils-14_larger_size.c \
	utils-15_put_size_t_fd.c \
	utils-16_print_size_line.c

COMMON_SRCS := \
	1_main.c \
	2_parse_main.c \
	2-1_parse_number.c \
	2-2_parse_stack.c \
	4_sort_main.c \
	4-1_simple_sort.c \
	4-2_medium_sort.c \
	4-3_radix_sort.c \
	5_sort_opticsri_main.c \
	5-1_sort_opticsri_calc.c \
	5-2_sort_opticsri_exec.c \
	utils-1_is_option.c \
	utils-2_strings_are_equal.c \
	utils-3_is_space.c \
	utils-4_print_error_and_free.c \
	utils-6_free.c \
	utils-7_rank_sort.c \
	utils-7-1_rank_assign.c \
	utils-8_print_operation.c \
	utils-9_swap_stack.c \
	utils-10_push_stack.c \
	utils-11_rotate_stack.c \
	utils-12_reverse_rotate_stack.c \
	utils-13_find_maximum_position.c \
	utils-14_larger_size.c

BONUS_SRCS := bonus-checker.c

OBJS := $(SRCS:.c=.o)
COMMON_OBJS := $(COMMON_SRCS:.c=.o)
BONUS_OBJS := $(BONUS_SRCS:.c=.o)

all: $(NAME)
	@echo "make up now!"

$(NAME): $(OBJS) $(LIBFT) $(PRINTF)
	@$(CC) $(CFLAGS) $(OBJS) $(LIBFT) $(PRINTF) -o $(NAME)

$(LIBFT):
	@$(MAKE) -s --no-print-directory -C $(LIBFT_DIR)

$(PRINTF):
	@$(MAKE) -s --no-print-directory -C $(PRINTF_DIR)

%.o: %.c push_swap.h
	@$(CC) $(CFLAGS) -c $< -o $@

bonus: $(BONUS_NAME)
	@echo "making bonus now!"

$(BONUS_NAME): $(COMMON_OBJS) $(BONUS_OBJS) $(LIBFT) $(PRINTF)
	@$(CC) $(CFLAGS) $(COMMON_OBJS) $(BONUS_OBJS) \
		$(LIBFT) $(PRINTF) -o $(BONUS_NAME)

clean:
	@echo "clean up now!"
	@$(MAKE) -s --no-print-directory clean_files

clean_files:
	@rm -f $(OBJS) $(BONUS_OBJS)
	@$(MAKE) -s --no-print-directory -C $(LIBFT_DIR) clean
	@$(MAKE) -s --no-print-directory -C $(PRINTF_DIR) clean

fclean:
	@echo "full clean up now!"
	@$(MAKE) -s --no-print-directory fclean_files

fclean_files:
	@rm -f $(OBJS) $(BONUS_OBJS) $(NAME) $(BONUS_NAME)
	@$(MAKE) -s --no-print-directory -C $(LIBFT_DIR) fclean
	@$(MAKE) -s --no-print-directory -C $(PRINTF_DIR) fclean

re:
	@echo "remaking now!"
	@$(MAKE) -s --no-print-directory fclean_files
	@$(MAKE) -s --no-print-directory $(NAME)

.PHONY: all bonus clean clean_files fclean fclean_files re
