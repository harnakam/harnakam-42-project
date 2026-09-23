/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_printf_print.c                                 :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:17:30 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_pf_putchar(char c)
{
	if (write(1, &c, 1) != 1)
		return (-1);
	return (1);
}

int	ft_pf_putstr(char *s)
{
	int	count;
	int	ret;

	if (s == 0)
		s = "(null)";
	count = 0;
	while (*s != '\0')
	{
		ret = ft_pf_putchar(*s);
		if (ret < 0)
			return (-1);
		count += ret;
		s++;
	}
	return (count);
}
