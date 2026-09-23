/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   5-1_sort_opticsri_calc.c                          :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:34 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	opticsri_sort(t_program *program)
{
	if (assign_rank_indexes(program) == ERROR)
		return ;
	move_all_optimally_to_stack_b(program);
	restore_stack_a(program);
}

void	move_all_optimally_to_stack_b(t_program *program)
{
	t_move	move;

	while (program->size_a > 0)
	{
		move = choose_move(program);
		execute_move(program, move);
	}
}

void	restore_stack_a(t_program *program)
{
	size_t	position;
	size_t	steps;

	position = find_maximum_position(program->stack_b);
	if (position <= program->size_b / 2)
	{
		while (position-- > 0)
			op_rb(program);
	}
	else
	{
		steps = program->size_b - position;
		while (steps-- > 0)
			op_rrb(program);
	}
	while (program->size_b > 0)
		op_pa(program);
}
