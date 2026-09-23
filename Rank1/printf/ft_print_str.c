/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_print_str.c                                    :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/24 16:18:24 by harnakam         #+#    #+#              */
/*   Updated: 2026/05/24 20:28:27 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_print_str(char *s)
{
	int	count;
	int	ret;

	count = 0;
	if (!s)
		s = "(null)";
	while (*s)
	{
		ret = ft_print_char(*s);
		if (ret < 0)
			return (-1);
		count += ret;
		s++;
	}
	return (count);
}

// int	main(void)
// {
// 	ft_print_str("Hello, World!");
// 	ft_print_char('\n');
// 	ft_print_str(NULL);
// 	ft_print_char('\n');
// 	return (0);
// }

// ccw ft_print_str.c ft_print_char.c
