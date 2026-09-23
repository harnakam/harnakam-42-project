/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_strjoin.c                                      :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/04/26 13:09:47 by harnakam         #+#    #+#              */
/*   Updated: 2026/04/26 13:09:47 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strjoin(char const *s1, char const *s2)
{
	char	*p;
	size_t	l1;
	size_t	l2;

	if (!s1 || !s2)
		return (NULL);
	l1 = ft_strlen(s1);
	l2 = ft_strlen(s2);
	p = (char *) malloc(sizeof(char) * (l1 + l2 + 1));
	if (p)
	{
		ft_strlcpy(p, s1, l1 + 1);
		ft_strlcat(p, s2, l1 + l2 + 1);
	}
	return (p);
}
