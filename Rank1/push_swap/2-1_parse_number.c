/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   2-1_parse_number.c                                :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:39 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	read_integer_sign(const char *string, size_t *position)
{
	int	sign;

	sign = 1;
	if (string[*position] == '+' || string[*position] == '-')
	{
		if (string[*position] == '-')
			sign = -1;
		(*position)++;
	}
	return (sign);
}

int	read_integer_digits(const char *string, size_t length, int sign,
		long *number)
{
	size_t	position;

	*number = 0;
	position = 0;
	while (position < length)
	{
		if (!ft_isdigit((unsigned char) string[position]))
			return (ERROR);
		*number = *number * 10 + (string[position] - '0');
		if (sign == 1 && *number > INT_MAX)
			return (ERROR);
		if (sign == -1 && *number > -(long) INT_MIN)
			return (ERROR);
		position++;
	}
	return (SUCCESS);
}

int	parse_integer(const char *string, size_t length, int *result)
{
	long	number;
	int		sign;
	size_t	i;

	if (length == 0)
		return (ERROR);
	i = 0;
	sign = read_integer_sign(string, &i);
	if (i == length)
		return (ERROR);
	if (read_integer_digits(string + i, length - i, sign, &number) == ERROR)
		return (ERROR);
	*result = (int)(number * sign);
	return (SUCCESS);
}

int	value_already_exists(const t_program *program, int value)
{
	t_node	*current;

	current = program->stack_a;
	while (current != NULL)
	{
		if (current->value == value)
			return (1);
		current = current->next;
	}
	return (0);
}
