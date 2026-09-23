/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   utils-16_print_size_line.c                        :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:14 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	print_size_line(const char *label, size_t number)
{
	ft_putstr_fd((char *) label, 2);
	put_size_t_fd(number, 2);
	ft_putchar_fd('\n', 2);
}
