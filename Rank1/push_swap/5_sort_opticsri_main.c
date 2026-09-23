/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   5_sort_opticsri_main.c                            :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:35 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_move	make_move(t_program *program, size_t a_position,
	size_t	b_position, int mode)
{
	t_move	move;

	move.a_reverse = (mode == 1 || mode == 3);
	move.b_reverse = (mode == 1 || mode == 2);
	move.a_steps = a_position;
	move.b_steps = b_position;
	if (move.a_reverse && a_position != 0)
		move.a_steps = program->size_a - a_position;
	if (move.b_reverse && b_position != 0)
		move.b_steps = program->size_b - b_position;
	if (move.a_reverse == move.b_reverse)
		move.cost = larger_size(move.a_steps, move.b_steps);
	else
		move.cost = move.a_steps + move.b_steps;
	return (move);
}

void	execute_move(t_program *program, t_move move)
{
	execute_shared_rotations(program, &move);
	while (move.a_steps-- > 0)
	{
		if (move.a_reverse)
			op_rra(program);
		else
			op_ra(program);
	}
	while (move.b_steps-- > 0)
	{
		if (move.b_reverse)
			op_rrb(program);
		else
			op_rb(program);
	}
	op_pb(program);
}

void	execute_shared_rotations(t_program *program, t_move *move)
{
	while (move->a_steps > 0 && move->b_steps > 0
		&& move->a_reverse == move->b_reverse)
	{
		if (move->a_reverse)
			op_rrr(program);
		else
			op_rr(program);
		move->a_steps--;
		move->b_steps--;
	}
}
