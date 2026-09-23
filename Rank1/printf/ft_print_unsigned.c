/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_print_unsigned.c                               :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/24 17:08:31 by harnakam         #+#    #+#              */
/*   Updated: 2026/05/24 20:28:49 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_print_unsigned(unsigned int n)
{
	int	count;
	int	ret;

	count = 0;
	if (n >= 10)
	{
		ret = ft_print_unsigned(n / 10);
		if (ret < 0)
			return (-1);
		count += ret;
	}
	ret = ft_print_char(n % 10 + '0');
	if (ret < 0)
		return (-1);
	return (count + ret);
}

// int	main(void)
// {
// 	ft_print_unsigned(42);
// 	ft_print_char('\n');
// 	ft_print_unsigned(0);
// 	ft_print_char('\n');
// 	ft_print_unsigned(4294967295u);
// 	ft_print_char('\n');
// }

// ccw ft_print_unsigned.c ft_print_char.c ft_print_nbr.c
