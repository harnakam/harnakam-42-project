/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   push_swap.c                                       :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:29 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	main(int argc, char **argv)
{
	t_program	program;

	if (argc == 1)
		return (0);
	initialize_program(&program, argc, argv);
	if (process_input(&program) == ERROR)
		return (print_error_and_free(&program));
	if (stack_a_is_empty(&program))
		return (free_all_and_exit_success(&program));
	compute_and_save_initial_disorder(&program);
	select_strategy(&program);
	if (!stack_a_is_sorted(&program))
		run_selected_strategy(&program);
	if (program.bench_enabled)
		print_benchmark_if_enabled(&program);
	else
		print_debug_if_enabled(&program);
	free_all(&program);
	return (0);
}

void	print_debug_if_enabled(const t_program *program)
{
	if (!program->debug_enabled)
		return ;
	ft_putstr_fd("Strategy: ", STDERR_FILENO);
	ft_putendl_fd((char *) get_strategy_name(
			program->selected_strategy), STDERR_FILENO);
	print_size_line("Total: ", program->operations.total);
}
