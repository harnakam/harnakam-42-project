/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_print_nbr.c                                    :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/24 16:25:46 by harnakam         #+#    #+#              */
/*   Updated: 2026/05/24 20:29:20 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_print_nbr(int n)
{
	long	num;
	int		count;
	int		ret;

	num = n;
	count = 0;
	if (num < 0)
	{
		ret = ft_print_char('-');
		if (ret < 0)
			return (-1);
		count += ret;
		num = -num;
	}
	if (num >= 10)
	{
		ret = ft_print_nbr(num / 10);
		if (ret < 0)
			return (-1);
		count += ret;
	}
	ret = ft_print_char(num % 10 + '0');
	if (ret < 0)
		return (-1);
	return (count + ret);
}

// int	main(void)
// {
// 	ft_print_nbr(42);
// 	ft_print_char('\n');
// 	ft_print_nbr(-42);
// 	ft_print_char('\n');
// 	ft_print_nbr(0);
// 	ft_print_char('\n');
// 	ft_print_nbr(-2147483648);
// 	ft_print_char('\n');
// }

// ccw ft_print_nbr.c ft_print_char.c
