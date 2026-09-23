/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_itoa.c                                         :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/04/26 13:08:53 by harnakam         #+#    #+#              */
/*   Updated: 2026/05/06 18:38:02 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static size_t	get_len(long n)
{
	size_t	len;

	len = 0;
	if (n <= 0)
	{
		len++;
		n = -n;
	}
	while (n)
	{
		len++;
		n /= 10;
	}
	return (len);
}

char	*ft_itoa(int n)
{
	char	*p;
	size_t	len;
	long	num;

	num = n;
	len = get_len(num);
	p = (char *) malloc(sizeof(char) * (len + 1));
	if (!p)
		return (NULL);
	p[len] = '\0';
	if (num == 0)
		p[0] = '0';
	if (num < 0)
	{
		p[0] = '-';
		num = -num;
	}
	while (num)
	{
		p[--len] = (num % 10) + '0';
		num /= 10;
	}
	return (p);
}
