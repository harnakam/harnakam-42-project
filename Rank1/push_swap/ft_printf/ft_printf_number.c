/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_printf_number.c                                :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:17:29 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	ft_putbase(unsigned long n, char *base, unsigned long base_len)
{
	int	count;
	int	ret;

	count = 0;
	if (n >= base_len)
	{
		ret = ft_putbase(n / base_len, base, base_len);
		if (ret < 0)
			return (-1);
		count += ret;
	}
	ret = ft_pf_putchar(base[n % base_len]);
	if (ret < 0)
		return (-1);
	return (count + ret);
}

int	ft_pf_putnbr(int n)
{
	long	nb;
	int		count;
	int		ret;

	nb = n;
	count = 0;
	if (nb < 0)
	{
		ret = ft_pf_putchar('-');
		if (ret < 0)
			return (-1);
		count += ret;
		nb = -nb;
	}
	ret = ft_putbase((unsigned long) nb, "0123456789", 10);
	if (ret < 0)
		return (-1);
	return (count + ret);
}

int	ft_pf_putunsigned(unsigned int n)
{
	return (ft_putbase(n, "0123456789", 10));
}

int	ft_pf_puthex(unsigned int n, char upper)
{
	if (upper)
		return (ft_putbase(n, "0123456789ABCDEF", 16));
	return (ft_putbase(n, "0123456789abcdef", 16));
}

int	ft_pf_putptr(void *ptr)
{
	unsigned long	addr;
	int				count;
	int				ret;

	if (ptr == 0)
		return (ft_pf_putstr("(nil)"));
	addr = (unsigned long) ptr;
	count = ft_pf_putstr("0x");
	if (count < 0)
		return (-1);
	ret = ft_putbase(addr, "0123456789abcdef", 16);
	if (ret < 0)
		return (-1);
	return (count + ret);
}
