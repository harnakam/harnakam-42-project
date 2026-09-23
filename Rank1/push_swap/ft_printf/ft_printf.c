/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_printf.c                                       :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:17:30 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	ft_print_unknown(char c)
{
	int	count;
	int	ret;

	count = ft_pf_putchar('%');
	if (count < 0)
		return (-1);
	ret = ft_pf_putchar(c);
	if (ret < 0)
		return (-1);
	return (count + ret);
}

static int	ft_print_conversion(char c, va_list args)
{
	if (c == 'c')
		return (ft_pf_putchar((char) va_arg(args, int)));
	if (c == 's')
		return (ft_pf_putstr(va_arg(args, char *)));
	if (c == 'p')
		return (ft_pf_putptr(va_arg(args, void *)));
	if (c == 'd' || c == 'i')
		return (ft_pf_putnbr(va_arg(args, int)));
	if (c == 'u')
		return (ft_pf_putunsigned(va_arg(args, unsigned int)));
	if (c == 'x' || c == 'X')
		return (ft_pf_puthex(va_arg(args, unsigned int), c == 'X'));
	if (c == '%')
		return (ft_pf_putchar('%'));
	return (ft_print_unknown(c));
}

static int	ft_append_count(int *total, int printed)
{
	if (printed < 0)
		return (-1);
	*total += printed;
	return (0);
}

int	ft_printf(const char *format, ...)
{
	va_list	args;
	int		total;
	int		printed;

	if (format == 0)
		return (-1);
	total = 0;
	va_start(args, format);
	while (*format != '\0')
	{
		if (*format == '%')
		{
			format++;
			if (*format == '\0')
				break ;
			printed = ft_print_conversion(*format, args);
		}
		else
			printed = ft_pf_putchar(*format);
		if (ft_append_count(&total, printed) < 0)
			return (va_end(args), -1);
		format++;
	}
	va_end(args);
	return (total);
}
