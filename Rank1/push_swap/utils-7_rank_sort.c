/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   utils-7_rank_sort.c                               :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:22 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	assign_rank_indexes(t_program *program)
{
	int	*values;
	int	*temporary;

	values = malloc(program->size_a * sizeof(*values));
	temporary = malloc(program->size_a * sizeof(*temporary));
	if (values == NULL || temporary == NULL)
		return (free(values), free(temporary), ERROR);
	copy_stack_values(program->stack_a, values);
	merge_sort_values(values, temporary, 0, program->size_a);
	assign_node_ranks(program->stack_a, values, program->size_a);
	free(values);
	free(temporary);
	return (SUCCESS);
}

void	merge_values(int *values, int *temporary, size_t left, size_t right)
{
	size_t	i;
	size_t	j;
	size_t	position;
	size_t	middle;

	middle = left + (right - left) / 2;
	i = left;
	j = middle;
	position = left;
	while (i < middle && j < right)
	{
		if (values[i] < values[j])
			temporary[position++] = values[i++];
		else
			temporary[position++] = values[j++];
	}
	while (i < middle)
		temporary[position++] = values[i++];
	while (j < right)
		temporary[position++] = values[j++];
	copy_merged_values(values, temporary, left, right);
}

void	copy_merged_values(int *values, const int *temporary,
	size_t	left, size_t right)
{
	while (left < right)
	{
		values[left] = temporary[left];
		left++;
	}
}

void	merge_sort_values(int *values, int *temporary, size_t left,
	size_t	right)
{
	size_t	middle;

	if (right - left < 2)
		return ;
	middle = left + (right - left) / 2;
	merge_sort_values(values, temporary, left, middle);
	merge_sort_values(values, temporary, middle, right);
	merge_values(values, temporary, left, right);
}
