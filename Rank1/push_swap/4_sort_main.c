/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   4_sort_main.c                                     :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:37 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	stack_a_is_sorted(const t_program *program)
{
	t_node	*current;

	current = program->stack_a;
	while (current != NULL && current->next != NULL)
	{
		if (current->value > current->next->value)
			return (0);
		current = current->next;
	}
	return (1);
}

void	run_selected_strategy(t_program *program)
{
	if (program->selected_strategy == STRATEGY_SIMPLE)
		spin_bubble_sort(program);
	else if (program->selected_strategy == STRATEGY_MEDIUM)
		spin_run_insertion(program);
	else if (program->selected_strategy == STRATEGY_COMPLEX)
		radix_sort(program);
	else if (program->selected_strategy == STRATEGY_ULTRA)
		opticsri_sort(program);
}
