/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   4-3_radix_sort.c                                  :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:35 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	radix_sort(t_program *program)
{
	size_t	bit;
	size_t	bits;

	if (assign_rank_indexes(program) == ERROR)
		return ;
	bits = count_rank_bits(program->size_a);
	bit = 0;
	while (bit < bits && !stack_a_is_sorted(program))
		radix_pass(program, bit++);
}

size_t	count_rank_bits(size_t size)
{
	size_t	bits;

	bits = 0;
	while (((size - 1) >> bits) != 0)
		bits++;
	return (bits);
}

void	radix_pass(t_program *program, size_t bit)
{
	size_t	i;
	size_t	size;

	i = 0;
	size = program->size_a;
	while (i++ < size)
	{
		if (((program->stack_a->index >> bit) & 1) == 0)
			op_pb(program);
		else
			op_ra(program);
	}
	while (program->size_b > 0)
		op_pa(program);
}
