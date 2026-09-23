/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   3_strategy.c                                      :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:37 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	stack_a_is_empty(const t_program *program)
{
	return (program->stack_a == NULL);
}

void	compute_and_save_initial_disorder(t_program *program)
{
	size_t	total_pairs;
	size_t	inversions;

	if (program->size_a <= 1)
	{
		program->initial_disorder = 0.0;
		return ;
	}
	total_pairs = program->size_a * (program->size_a - 1) / 2;
	inversions = count_inversions(program->stack_a);
	program->initial_disorder = (double) inversions / (double) total_pairs;
}

size_t	count_inversions(const t_node *stack)
{
	const t_node	*first;
	const t_node	*second;
	size_t			inversions;

	inversions = 0;
	first = stack;
	while (first != NULL)
	{
		second = first->next;
		while (second != NULL)
		{
			if (first->value > second->value)
				inversions++;
			second = second->next;
		}
		first = first->next;
	}
	return (inversions);
}

void	select_strategy(t_program *program)
{
	if (program->requested_strategy != STRATEGY_ADAPTIVE)
	{
		program->selected_strategy = program->requested_strategy;
		return ;
	}
	program->selected_strategy = select_adaptive_strategy(program);
}

t_strategy	select_adaptive_strategy(const t_program *program)
{
	if (program->size_a <= 5)
		return (STRATEGY_SIMPLE);
	if (program->initial_disorder < 0.20)
		return (STRATEGY_SIMPLE);
	if (program->initial_disorder < 0.50)
		return (STRATEGY_MEDIUM);
	return (STRATEGY_COMPLEX);
}
