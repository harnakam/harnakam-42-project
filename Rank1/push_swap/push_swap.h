/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   push_swap.h                                       :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:19:56 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <stdlib.h>
# include <unistd.h>
# include <limits.h>
# include "Libft/libft.h"
# include "ft_printf/ft_printf.h"

# define SUCCESS 0
# define ERROR 1

typedef enum e_strategy
{
	STRATEGY_NONE,
	STRATEGY_SIMPLE,
	STRATEGY_MEDIUM,
	STRATEGY_COMPLEX,
	STRATEGY_ADAPTIVE,
	STRATEGY_ULTRA
}	t_strategy;

typedef struct s_node
{
	int				value;
	int				index;
	struct s_node	*prev;
	struct s_node	*next;
}	t_node;

typedef struct s_operation_count
{
	size_t	sa;
	size_t	sb;
	size_t	ss;
	size_t	pa;
	size_t	pb;
	size_t	ra;
	size_t	rb;
	size_t	rr;
	size_t	rra;
	size_t	rrb;
	size_t	rrr;
	size_t	total;
}	t_operation_count;

typedef struct s_program
{
	int					argc;
	char				**argv;
	t_node				*stack_a;
	t_node				*stack_b;
	size_t				size_a;
	size_t				size_b;
	t_strategy			requested_strategy;
	t_strategy			selected_strategy;
	int					bench_enabled;
	int					debug_enabled;
	double				initial_disorder;
	t_operation_count	operations;
}	t_program;

typedef struct s_move
{
	size_t	a_steps;
	size_t	b_steps;
	size_t	cost;
	int		a_reverse;
	int		b_reverse;
}	t_move;

void		initialize_program(t_program *program, int argc, char **argv);
void		initialize_operation_count(t_operation_count *operations);
int			process_input(t_program *program);
int			parse_options(t_program *program);
int			parse_numbers_into_stack_a(t_program *program);
int			stack_a_is_empty(const t_program *program);
void		compute_and_save_initial_disorder(t_program *program);
size_t		count_inversions(const t_node *stack);
void		select_strategy(t_program *program);
t_strategy	select_adaptive_strategy(const t_program *program);
int			stack_a_is_sorted(const t_program *program);
void		run_selected_strategy(t_program *program);
void		print_benchmark_if_enabled(const t_program *program);
const char	*get_strategy_name(t_strategy strategy);
const char	*get_strategy_complexity(t_strategy strategy);
void		print_disorder(double disorder);
void		print_operation_counts(const t_operation_count *operations);
void		free_all(t_program *program);
void		free_stack(t_node **stack);

int			is_option(const char *argument);
int			strings_are_equal(const char *first, const char *second);
int			is_space(char character);
int			is_strategy_option(const char *argument);
t_strategy	get_strategy_from_option(const char *argument);
int			parse_one_option(t_program *program, const char *argument);
int			parse_integer(const char *string, size_t length, int *result);
int			read_integer_sign(const char *string, size_t *position);
int			read_integer_digits(const char *string, size_t length, int sign,
				long *number);
int			value_already_exists(const t_program *program, int value);
int			append_value_to_stack_a(t_program *program, int value);
int			parse_one_word(t_program *program, const char *start,
				size_t length);
int			parse_argument(t_program *program, const char *argument);

int			print_error_and_free(t_program *program);
int			free_all_and_exit_success(t_program *program);

void		spin_bubble_sort(t_program *program);
void		find_limits(t_program *program, int *minimum, int *maximum);
int			spin_bubble_pass(t_program *program, int minimum, int maximum);
void		spin_run_insertion(t_program *program);
size_t		chunk_width(size_t size);
void		move_runs_to_stack_b(t_program *program, size_t width);
void		move_maximum_to_top(t_program *program);
void		restore_runs_to_stack_a(t_program *program);
void		radix_sort(t_program *program);
size_t		count_rank_bits(size_t size);
void		radix_pass(t_program *program, size_t bit);
void		opticsri_sort(t_program *program);
void		move_all_optimally_to_stack_b(t_program *program);
t_move		choose_move(t_program *program);
t_move		choose_node_move(t_program *program, t_node *node,
				size_t a_position, t_move best);
size_t		insertion_position(t_program *program, int index);
t_move		make_move(t_program *program, size_t a_position,
				size_t b_position, int mode);
void		execute_move(t_program *program, t_move move);
void		execute_shared_rotations(t_program *program, t_move *move);
void		restore_stack_a(t_program *program);

void		print_operation(t_program *program, const char *name,
				size_t *counter);
void		swap_stack(t_node *stack);
void		push_stack(t_node **source, t_node **destination,
				size_t *source_size, size_t *destination_size);
void		rotate_stack(t_node **stack);
void		reverse_rotate_stack(t_node **stack);
void		op_sa(t_program *program);
void		op_sb(t_program *program);
void		op_pa(t_program *program);
void		op_pb(t_program *program);
void		op_ra(t_program *program);
void		op_rb(t_program *program);
void		op_rr(t_program *program);
void		op_rra(t_program *program);
void		op_rrb(t_program *program);
void		op_rrr(t_program *program);

int			assign_rank_indexes(t_program *program);
void		merge_values(int *values, int *temporary, size_t left,
				size_t right);
void		copy_merged_values(int *values, const int *temporary,
				size_t left, size_t right);
void		merge_sort_values(int *values, int *temporary, size_t left,
				size_t right);
int			find_rank(const int *values, size_t size, int value);
void		copy_stack_values(t_node *stack, int *values);
void		assign_node_ranks(t_node *stack, const int *values, size_t size);
size_t		find_maximum_position(t_node *stack);
size_t		larger_size(size_t first, size_t second);

void		put_size_t_fd(size_t number, int fd);
void		print_size_line(const char *label, size_t number);
void		print_debug_if_enabled(const t_program *program);

#endif
