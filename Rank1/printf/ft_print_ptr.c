/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_print_ptr.c                                    :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/24 18:14:18 by harnakam         #+#    #+#              */
/*   Updated: 2026/05/24 20:27:56 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_print_ptr(void *ptr)
{
	int	count;
	int	total_len;

	if (ptr == NULL)
		return (ft_print_str("(nil)"));
	count = 0;
	total_len = ft_print_char('0');
	if (total_len < 0)
		return (-1);
	count += total_len;
	total_len = ft_print_char('x');
	if (total_len < 0)
		return (-1);
	count += total_len;
	total_len = ft_putbase((unsigned long) ptr, "0123456789abcdef", 16);
	if (total_len < 0)
		return (-1);
	return (count + total_len);
}
