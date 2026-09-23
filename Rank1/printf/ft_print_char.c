/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_print_char.c                                   :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/24 16:14:47 by harnakam         #+#    #+#              */
/*   Updated: 2026/05/24 20:27:14 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_print_char(char c)
{
	if (write(1, &c, 1) != 1)
		return (-1);
	return (1);
}

// int	main(void)
// {
// 	int	len;

// 	len = ft_print_char('A');
// 	ft_print_char('\n');
// 	return (0);
// }

// ccw ft_print_char.c
