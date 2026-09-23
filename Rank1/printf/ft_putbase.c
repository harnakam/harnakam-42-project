/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_putbase.c                                      :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/24 17:16:21 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/02 18:30:06 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putbase(unsigned long n, char *base, unsigned long base_len)
{
	int	total_len;
	int	written;

	total_len = 0;
	if (n >= base_len)
	{
		written = ft_putbase(n / base_len, base, base_len);
		if (written < 0)
			return (-1);
		total_len += written;
	}
	written = ft_print_char(base[n % base_len]);
	if (written < 0)
		return (-1);
	return (total_len + written);
}
