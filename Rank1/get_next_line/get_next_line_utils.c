/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   get_next_line_utils.c                             :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/25 14:53:18 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/25 15:18:59 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

size_t	ft_strlen(const char *str)
{
	size_t	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

static size_t	get_stash_len(char *stash)
{
	if (stash == NULL)
		return (0);
	return (ft_strlen(stash));
}

char	*ft_strchr(const char *str, int c)
{
	while (str != NULL && *str != '\0')
	{
		if (*str == (char) c)
			return ((char *) str);
		str++;
	}
	if (str != NULL && (char) c == '\0')
		return ((char *) str);
	return (NULL);
}

char	*ft_strjoin_free(char *stash, const char *buffer)
{
	char	*joined;
	size_t	i;
	size_t	j;

	joined = malloc(get_stash_len(stash) + ft_strlen(buffer) + 1);
	if (joined == NULL)
	{
		free(stash);
		return (NULL);
	}
	i = 0;
	while (stash != NULL && stash[i] != '\0')
	{
		joined[i] = stash[i];
		i++;
	}
	j = 0;
	while (buffer[j] != '\0')
		joined[i++] = buffer[j++];
	joined[i] = '\0';
	free(stash);
	return (joined);
}
