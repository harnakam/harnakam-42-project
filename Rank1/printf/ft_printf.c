/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_printf.c                                       :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/24 18:13:25 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/02 18:49:52 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	ft_print_unknown(char c)
{
	int	percent_len;
	int	char_len;

	percent_len = ft_print_char('%');
	if (percent_len < 0)
		return (-1);
	char_len = ft_print_char(c);
	if (char_len < 0)
		return (-1);
	return (percent_len + char_len);
}

static int	ft_print_format(char type, va_list args)
{
	if (type == 'c')
		return (ft_print_char(va_arg(args, int)));
	if (type == 's')
		return (ft_print_str(va_arg(args, char *)));
	if (type == 'p')
		return (ft_print_ptr(va_arg(args, void *)));
	if (type == 'd' || type == 'i')
		return (ft_print_nbr(va_arg(args, int)));
	if (type == 'u')
		return (ft_print_unsigned(va_arg(args, unsigned int)));
	if (type == 'x')
		return (ft_print_hex(va_arg(args, unsigned int), 0));
	if (type == 'X')
		return (ft_print_hex(va_arg(args, unsigned int), 1));
	if (type == '%')
		return (ft_print_char('%'));
	if (type == 'a')
		return (ft_print_str("my awsome 42"));
	return (ft_print_unknown(type));
}

static int	ft_add_count(int *total, int printed)
{
	if (printed < 0)
		return (-1);
	*total += printed;
	return (0);
}

int	ft_printf(const char *format, ...)
{
	int		total;
	int		printed;
	va_list	args;

	if (!format)
		return (-1);
	total = 0;
	va_start(args, format);
	while (*format)
	{
		if (*format == '%')
		{
			format++;
			if (!*format)
				break ;
			printed = ft_print_format(*format, args);
		}
		else
			printed = ft_print_char(*format);
		if (ft_add_count(&total, printed) < 0)
			return (va_end(args), -1);
		format++;
	}
	va_end(args);
	return (total);
}

// int	main(void)
// {
// 	int	a;

// 	a = ft_printf("Hello %a World\n");
// 	ft_printf("%d", a);
// }
