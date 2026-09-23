/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   utils-10_push_stack.c                             :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:19 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	push_stack(t_node **source, t_node **destination,
	size_t	*source_size, size_t *destination_size)
{
	t_node	*node;

	if (*source == NULL)
		return ;
	node = *source;
	*source = node->next;
	if (*source != NULL)
		(*source)->prev = NULL;
	node->prev = NULL;
	node->next = *destination;
	if (*destination != NULL)
		(*destination)->prev = node;
	*destination = node;
	(*source_size)--;
	(*destination_size)++;
}

void	op_pa(t_program *program)
{
	if (program->size_b == 0)
		return ;
	push_stack(&program->stack_b, &program->stack_a,
		&program->size_b, &program->size_a);
	print_operation(program, "pa", &program->operations.pa);
}

void	op_pb(t_program *program)
{
	if (program->size_a == 0)
		return ;
	push_stack(&program->stack_a, &program->stack_b,
		&program->size_a, &program->size_b);
	print_operation(program, "pb", &program->operations.pb);
}
