/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   utils-11_rotate_stack.c                           :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:18 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	rotate_stack(t_node **stack)
{
	t_node	*first;
	t_node	*last;

	if (*stack == NULL || (*stack)->next == NULL)
		return ;
	first = *stack;
	*stack = first->next;
	(*stack)->prev = NULL;
	last = *stack;
	while (last->next != NULL)
		last = last->next;
	last->next = first;
	first->prev = last;
	first->next = NULL;
}

void	op_ra(t_program *program)
{
	if (program->size_a < 2)
		return ;
	rotate_stack(&program->stack_a);
	print_operation(program, "ra", &program->operations.ra);
}

void	op_rb(t_program *program)
{
	if (program->size_b < 2)
		return ;
	rotate_stack(&program->stack_b);
	print_operation(program, "rb", &program->operations.rb);
}

void	op_rr(t_program *program)
{
	if (program->size_a < 2 || program->size_b < 2)
		return ;
	rotate_stack(&program->stack_a);
	rotate_stack(&program->stack_b);
	print_operation(program, "rr", &program->operations.rr);
}
