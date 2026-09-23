/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   utils-9_swap_stack.c                              :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:19 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	swap_stack(t_node *stack)
{
	int	value;
	int	index;

	if (stack == NULL || stack->next == NULL)
		return ;
	value = stack->value;
	index = stack->index;
	stack->value = stack->next->value;
	stack->index = stack->next->index;
	stack->next->value = value;
	stack->next->index = index;
}

void	op_sa(t_program *program)
{
	if (program->size_a < 2)
		return ;
	swap_stack(program->stack_a);
	print_operation(program, "sa", &program->operations.sa);
}

void	op_sb(t_program *program)
{
	if (program->size_b < 2)
		return ;
	swap_stack(program->stack_b);
	print_operation(program, "sb", &program->operations.sb);
}
