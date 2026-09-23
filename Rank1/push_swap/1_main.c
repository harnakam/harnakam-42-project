/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   1_main.c                                          :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:27:41 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	initialize_program(t_program *program, int argc, char **argv)
{
	program->argc = argc;
	program->argv = argv;
	program->stack_a = NULL;
	program->stack_b = NULL;
	program->size_a = 0;
	program->size_b = 0;
	program->requested_strategy = STRATEGY_NONE;
	program->selected_strategy = STRATEGY_NONE;
	program->bench_enabled = 0;
	program->debug_enabled = 0;
	program->initial_disorder = 0.0;
	initialize_operation_count(&program->operations);
}

void	initialize_operation_count(t_operation_count *operations)
{
	ft_bzero(operations, sizeof(*operations));
}
