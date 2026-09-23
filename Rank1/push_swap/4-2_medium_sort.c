/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   4-2_medium_sort.c                                 :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:36 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	spin_run_insertion(t_program *program)
{
	size_t	width;

	if (assign_rank_indexes(program) == ERROR)
		return ;
	width = chunk_width(program->size_a);
	move_runs_to_stack_b(program, width);
	restore_runs_to_stack_a(program);
}

size_t	chunk_width(size_t size)
{
	size_t	width;

	width = 1;
	while (width * width < size)
		width++;
	return (width);
}

void	move_maximum_to_top(t_program *program)
{
	size_t	position;
	size_t	steps;

	position = find_maximum_position(program->stack_b);
	if (position <= program->size_b / 2)
		while (position-- > 0)
			op_rb(program);
	else
	{
		steps = program->size_b - position;
		while (steps-- > 0)
			op_rrb(program);
	}
}

void	restore_runs_to_stack_a(t_program *program)
{
	while (program->size_b > 0)
	{
		move_maximum_to_top(program);
		op_pa(program);
	}
}

void	move_runs_to_stack_b(t_program *program, size_t width)
{
	size_t	accepted;

	accepted = 0;
	while (program->size_a > 0)
	{
		if ((size_t) program->stack_a->index <= accepted)
		{
			op_pb(program);
			op_rb(program);
			accepted++;
		}
		else if ((size_t) program->stack_a->index <= accepted + width)
		{
			op_pb(program);
			accepted++;
		}
		else
			op_ra(program);
	}
}
