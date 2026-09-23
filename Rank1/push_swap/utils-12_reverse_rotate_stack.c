/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   utils-12_reverse_rotate_stack.c                   :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:17 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	reverse_rotate_stack(t_node **stack)
{
	t_node	*last;

	if (*stack == NULL || (*stack)->next == NULL)
		return ;
	last = *stack;
	while (last->next != NULL)
		last = last->next;
	last->prev->next = NULL;
	last->prev = NULL;
	last->next = *stack;
	(*stack)->prev = last;
	*stack = last;
}

void	op_rra(t_program *program)
{
	if (program->size_a < 2)
		return ;
	reverse_rotate_stack(&program->stack_a);
	print_operation(program, "rra", &program->operations.rra);
}

void	op_rrb(t_program *program)
{
	if (program->size_b < 2)
		return ;
	reverse_rotate_stack(&program->stack_b);
	print_operation(program, "rrb", &program->operations.rrb);
}

void	op_rrr(t_program *program)
{
	if (program->size_a < 2 || program->size_b < 2)
		return ;
	reverse_rotate_stack(&program->stack_a);
	reverse_rotate_stack(&program->stack_b);
	print_operation(program, "rrr", &program->operations.rrr);
}
