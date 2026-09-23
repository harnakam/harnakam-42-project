/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_print_hex.c                                    :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/24 17:50:08 by harnakam         #+#    #+#              */
/*   Updated: 2026/05/24 18:05:42 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_print_hex(unsigned int n, int upper)
{
	if (upper)
		return (ft_putbase(n, "0123456789ABCDEF", 16));
	return (ft_putbase(n, "0123456789abcdef", 16));
}
